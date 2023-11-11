import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CognitoIdentityCredentials } from 'aws-sdk/global';
import AWS from 'aws-sdk';
import { v4 } from 'uuid';
import { get_image } from './LaTeXInput';

// Constants for Amazon Cognito Identity Pool
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID
const REGION = process.env.REACT_APP_REGION;
const S3_BUCKET = process.env.REACT_APP_S3_BUCKET;

AWS.config.region = REGION;

// Initialize the Amazon Cognito credentials provider
AWS.config.credentials = new CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

function UploadPDFToS3WithNativeSdk() {
  const navigate = useNavigate();
  const toReturnPage = () => {
    navigate('/returnpage', { state: { selectedFile: selectedFile } })
  }


  const [selectedFile, setSelectedFile] = useState(null);
  const [progress, setProgress] = useState(0);

  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadFile = (file) => {
    AWS.config.credentials.get((err) => {
      if (err) {
        console.log("Error retrieving credentials: ", err);
        return;
      }

      const myBucket = new AWS.S3({
        params: { Bucket: S3_BUCKET },
        region: REGION,
      });

      // const mySQS = new AWS.SQS({
      //   params: {
      //     QueueUrl: process.env.REACT_APP_SQS_URL
      //   },
      //   region: REGION
      // })

      const uuidKey = v4();
      const fileKey = 'inputs/' + uuidKey + '_pdf';
      const imageKey = 'inputs/' + uuidKey + '_image';

      const imageURL = get_image();

      fetch(imageURL)
        .then(response => response.blob())
        .then(blob => {
          const imageParams = {
            ACL: 'public-read',
            Body: blob,
            Bucket: S3_BUCKET,
            Key: imageKey
          };

          myBucket.putObject(imageParams)
            .on('httpUploadProgress', (evt) => {
              setProgress(Math.round((evt.loaded / evt.total) * 100));
            })
            .send((err) => {
              if (err) console.log(err)
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
              setProgress(Math.round((evt.loaded / evt.total) * 100));
            })
            .send((err) => {
              if (err) console.log(err)
            });

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
          fetch(process.env.REACT_APP_UPLOAD, requestOptions)
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
              console.log(response)
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
    });
  };

  return (
    <div>
      <div>Native SDK File Upload Progress is {progress}%</div>
      <input id="file_input" type="file" onChange={handleFileInput} />
      <button onClick={() => uploadFile(selectedFile)}>Upload to S3</button>
    </div>
  );
}

export default UploadPDFToS3WithNativeSdk;
