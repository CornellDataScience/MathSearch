import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import AWS from 'aws-sdk'
import fs from 'fs';
import {v4} from 'uuid';
import {get_image} from './LaTeXInput'

const S3_BUCKET = 'mathsearch-intermediary'
const REGION = 'us-east-1';

const keyprefix = 'inputs/';

const bucketName = 'mathsearch-intermediary';
const objectKey = 'sample_hw1.txt';
// const fileKey = '/home/ubuntu/MathSearch/front-end/mathsearch/src/components/pages/sample_hw1.pdf'
const fileData = fs.readFileSync('/home/ubuntu/MathSearch/front-end/mathsearch/src/components/pages/sample_hw1.pdf');

const s3 = new AWS.S3({
  region: REGION,
  credentials: new AWS.EC2MetadataCredentials({
    httpOptions: { timeout: 5000 }, // optional timeout
    maxRetries: 10, // optional retry limit
    retryDelayOptions: { base: 200 } // optional retry delay
  })
});

// var tempCreds = new AWS.ChainableTemporaryCredentials({
//   params: {
//     RoleArn: 'arn:aws:iam::290365077634:role/ec2_access_s3'
//   }
// });

// console.log(tempCreds.getPromise());

// AWS.config.update({
//   accessKeyId: process.env.REACT_APP_ACCESS_KEY_ID,
//   secretAccessKey: process.env.REACT_APP_SECRET_ACCESS_KEY
// })


// const myBucket = new AWS.S3({
//   params: {
//     Bucket: S3_BUCKET
//   },
//   region: REGION
// })

const s3Endpoint = new AWS.Endpoint('s3-us-east-1.amazonaws.com');

const myBucket = new AWS.S3({
  region: REGION, endpoint: s3Endpoint
});

AWS.config.getCredentials(function(err) {
  if (err) console.log(err.stack);
  // credentials not loaded
  else {
    console.log("Access key:", AWS.config.credentials.accessKeyId);
  }
});

myBucket.listObjects({Bucket: S3_BUCKET}, function(err, data) {
  if (err) console.log(err, err.stack);
  else console.log(data);
});

// const mySQS = new AWS.SQS({
//   params: {
//     QueueUrl: process.env.REACT_APP_SQS_URL
//   },
//   region: REGION
// })

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
           Body: blob,
           Bucket: S3_BUCKET,
           Key: imageKey
         }
          myBucket.upload(imageParams, function(err, data) {
            if (err) {
              console.log('Error uploading file:', err);
            } else {
              console.log('File uploaded successfully:', data.Location);
            }
          });
          // myBucket.putObject(imageParams)
          //         .send((err) => {
          //           if (err) console.log(err)
          //         })

          s3.upload({
          Bucket: bucketName,
          Key: objectKey,
          Body: fileData
          }, function(err, data) {
          if (err) {
            console.log('Error uploading file:', err);
          } else {
            console.log('File uploaded successfully:', data.Location);
          }
        });
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

        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(msg)
      };
        fetch('http://18.206.12.64/run', requestOptions)
        .then(async response => {
            const isJson = response.headers.get('content-type')?.includes('application/json');
            const data = isJson && await response.json();

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response status
                const error = (data && data.message) || response.status;
                return Promise.reject(error);
            }

            console.log('Message sent to backend success!')
            console.log(response.data.message)
        })
        .catch(error => {
            // this.setState({ errorMessage: error.toString() });
            console.error('There was an error!', error);
        });

        // const sqsParams = {
        //   MessageBody: JSON.stringify(msg)
        // }

        // mySQS.sendMessage(sqsParams, function(err, data){
        //   if (err) {
        //     console.log("Error: ", err)
        //   } else {
        //     console.log("Success: ", data.MessageId);
        //   }
        // });

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
