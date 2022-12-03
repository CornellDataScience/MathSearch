import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import AWS from 'aws-sdk'
import {v4} from 'uuid';
import {get_image} from './LaTeXInput'

const S3_BUCKET = process.env.REACT_APP_S3_BUCKET;
const REGION = process.env.REACT_APP_REGION;

const keyprefix = 'inputs/';

AWS.config.update({
  accessKeyId: process.env.REACT_APP_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_SECRET_ACCESS_KEY
})

const myBucket = new AWS.S3({
  params: {
    Bucket: S3_BUCKET
  },
  region: REGION
})

const mySQS = new AWS.SQS({
  params: {
    QueueUrl: process.env.REACT_APP_SQS_URL
  },
  region: REGION
})

function UploadPDFToS3WithNativeSdk(){

  const navigate = useNavigate();

  const toReturnPage = () => {
    navigate('/returnpage', {state:{selectedFile: selectedFile}})
  }

  const [selectedFile, setSelectedFile] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  }

  function validateResponse(response) {
    if (!response.ok) {
        throw Error(response.statusText);
    }
    return response;
  }

  const uploadFile = async (file) => {
    const uuidKey = v4();
    const fileKey = keyprefix + uuidKey + "_pdf";
    const imageKey = keyprefix + uuidKey + "_image";

    var imageURL = get_image();

    console.log(imageURL);

    fetch(imageURL)
      .then(validateResponse)
      .then(response => response.blob())
      .then(blob => {
         const imageParams = {
           ACL: 'public-read',
           Body: blob,
           Bucket: S3_BUCKET,
           Key: imageKey
         }

          myBucket.putObject(imageParams)
                  .send((err) => {
                    if (err) console.log(err)
                  })
      })
      .then(() => {
        const pdfParams = {
          ACL: 'public-read',
          Body: file,
          Bucket: S3_BUCKET,
          Key: fileKey
        };

        myBucket.putObject(pdfParams)
                .on('httpUploadProgress', (evt) => {
                  setProgress(Math.round((evt.loaded / evt.total) * 100))
                })
                .send((err) => {
                  if (err) console.log(err)
                })

        let msg = {
          uuid: uuidKey,
          pdf_path: fileKey,
          image_path: imageKey
        }

        const sqsParams = {
          MessageBody: JSON.stringify(msg)
        }

        mySQS.sendMessage(sqsParams, function(err, data){
          if (err) {
            console.log("Error: ", err)
          } else {
            console.log("Success: ", data.MessageId);
          }
        });

        toReturnPage();

      });
  }


  return <div>
    <div>Native SDK File Upload Progress is {progress}%</div>
    <input id="file_input" type="file" onChange={handleFileInput} />
    <button onClick={() => uploadFile(selectedFile)}> Upload to S3</button>
  </div>
}

export default UploadPDFToS3WithNativeSdk;
