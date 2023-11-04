const AWS = require('aws-sdk');


const s3 = new AWS.S3({
  region: 'us-east-1'
});

const credentialProvider = new AWS.CredentialProviderChain();

credentialProvider.resolve((err, credentials) => {
  if (err) {
    console.error(err);
  } else {
    s3.getObject({
      Bucket: 'mathsearch-intermediary',
      Key: 'test.txt',
      Credentials: credentials
    }, (err, data) => {
      if (err) {
        console.error(err);
      } else {
        console.log(data.Body.toString());
      }
    });
  }
});



// const session = new AWS.Session({
//   profile: 'default'
// });

// const s3_session = new AWS.S3({
//   region: 'us-east-1', // replace with your region
//   credentials: session
// });

// const bucket = s3_session.Bucket('mathsearch-intermediary');
// bucket.objects().on('data', function(data) {
//   console.log(data.Key);
// }).on('end', function() {
//   console.log('Finished listing objects in bucket.');
// });





// AWS.config.credentials = new AWS.EnvironmentCredentials('AWS');
// const s3 = new AWS.S3();
// const params = {
//   Bucket: 'your_bucket_name',
//   Key: 'your_file_key'
// };

// s3.getObject(params, (err, data) => {
//   if (err) {
//     console.error(err);
//   } else {
//     console.log(data.Body.toString());
//   }
// });
