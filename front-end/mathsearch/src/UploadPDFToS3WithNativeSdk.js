import React, { useState } from 'react';
import AWS from 'aws-sdk'

const S3_BUCKET = 'mathsearch-intermediary';
const REGION = 'us-east-1';


AWS.config.update({
  accessKeyId: 'AKIAUHGY3PCBII4RLSOV',
  secretAccessKey: '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'
})

const myBucket = new AWS.S3({
  params: { Bucket: S3_BUCKET },
  region: REGION,
})

const UploadPDFToS3WithNativeSdk = () => {

  const [progress, setProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  }

  const uploadFile = (file) => {

    const params = {
      ACL: 'public-read',
      Body: file,
      Bucket: S3_BUCKET,
      Key: file.name
    };

    myBucket.putObject(params)
      .on('httpUploadProgress', (evt) => {
        setProgress(Math.round((evt.loaded / evt.total) * 100))
      })
      .send((err) => {
        if (err) console.log(err)
      })
  }


  return <div>
    <div>Native SDK File Upload Progress is {progress}%</div>
    <input type="file" onChange={handleFileInput} />
    <button onClick={() => uploadFile(selectedFile)}> Upload to S3</button>
  </div>
}

export default UploadPDFToS3WithNativeSdk;