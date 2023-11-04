import React, { useState } from 'react';
import {useNavigate} from 'react-router-dom';
import AWS from 'aws-sdk'
import {v4} from 'uuid';
import {get_image} from './LaTeXInput'
const fs = require('fs');

const S3_BUCKET = process.env.REACT_APP_S3_BUCKET;
const REGION = process.env.REACT_APP_REGION;

const keyprefix = 'inputs/';

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



const myBucket = new AWS.S3({
  params: {
    Bucket: S3_BUCKET
  },
  region: REGION
})

// myBucket.listObjects({Bucket: S3_BUCKET}, function(err, data) {
//   if (err) console.log(err, err.stack);
//   else console.log(data);
// });

const mySQS = new AWS.SQS({
  params: {
    QueueUrl: process.env.REACT_APP_SQS_URL
  },
  region: REGION
})

// Create an instance of the Lambda service
const lambda = new AWS.Lambda({
  region: 'us-east-1', // Replace with your desired AWS region
});

// Define the parameters to pass to the Lambda function
const params = {
  FunctionName: 'generatePresignedURL', // Replace with your Lambda function's name
  InvocationType: 'RequestResponse', // Can be 'RequestResponse' for synchronous invocation
  Payload: JSON.stringify({
    bucket: 'mathsearch-intermediary',
    key: 'inputs/',
  }),
};

lambda.invoke(params, (err, data) => {
  if (err) {
    console.error('Error invoking Lambda:', err);
  } else {
    const response = JSON.parse(data.Payload);
    console.log('Lambda Response:', response);

    // The presigned URL can be extracted from the Lambda response
    const presignedUrl = response.signedUrl;
    console.log('Presigned URL:', presignedUrl);

    // Now, you can use the presigned URL to upload a file to S3
    const filePath = 'path/to/your/file.ext'; // Replace with the path to your file
    const fileData = fs.readFileSync(filePath);

    myBucket.putObject({
      Bucket: 'mathsearch-intermediary', // Replace with your S3 bucket name
      Key: 'inputs/your-file-name.ext', // Replace with the desired S3 key (filename)
      Body: fileData,
      ContentType: 'application/octet-stream', // Replace with the appropriate content type
      ContentLength: fileData.length,
      ACL: 'public-read', // Set the desired access control list
    }, (s3Error, s3Data) => {
      if (s3Error) {
        console.error('Error uploading file to S3:', s3Error);
      } else {
        console.log('File uploaded successfully to S3:', s3Data);
      }
    });
  }
});

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

  const uploadFile = async (file) =>  {
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