import React, { useState } from 'react';
import ReactDOM from 'react-dom'
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';

import { useNavigate } from "react-router-dom";

import "./LaTeXInput.css";

function updatePreview() {
  let rawtext = document.getElementById('MathInput').value;
  ReactDOM.render(<BlockMath math={rawtext} />,
    document.getElementById('MathPreview'));
}

function get_image() {
  let tex = document.getElementById('MathInput').value;
  var url = "http://chart.apis.google.com/chart?&cht=tx&chl=" +
    encodeURIComponent(tex) +
    "&chof=png";
  return url;
}

function log_image() {
  let url = get_image();
  console.log(url);
}

/* BEGIN AWS CONSTANTS */

// Constants for Amazon Cognito Identity Pool
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID
const REGION = process.env.REACT_APP_REGION;
const S3_BUCKET = process.env.REACT_APP_S3_BUCKET;

AWS.config.region = REGION;

// Initialize the Amazon Cognito credentials provider
AWS.config.credentials = new CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

/* END AWS CONSTANTS */

function LaTeXInput() {
  const navigate = useNavigate()

  const [text, setText] = useState("")
  const [focus, setFocus] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null);

  const uploadRequest = (file, text) => {
    AWS.config.credentials.get((err) => {
      if (err) {
        console.log("Error retrieving credentials: ", err);
        return;
      }

      const myBucket = new AWS.S3({
        params: { Bucket: S3_BUCKET },
        region: REGION,
      });

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
        });
    });
  }

  const handleClick = async () => {
    // setLoading(true)
    // await new Promise(resolve => setTimeout(resolve, 5000));
    // redirect()

    // Send an API request with uploaded PDF blob
    // Current request is a placeholder, replace with something else later
    // const url = "http://mathsearch.org/api/send_request"
    // const response = await fetch(url);

    // Navigate to results page to wait for result
    uploadRequest(selectedFile, text)
    navigate('/results/request_id_here')
    // test_api()
  }

  // When user types in the search bar
  const handleChange = async (event) => {
    setText(event.target.value)
  }

  // When user clicks into the search bar
  const handleFocus = async (event) => {
    setFocus(true)
  }

  // When user clicks out of the search bar
  const handleBlur = async (event) => {
    setFocus(false)
  }

  // When user uploads a file
  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  return (
    <>
      <div className="latex-input-container">
        <div className="latex-input-content">
          {/* Math input */}
          <div className="input-group">
            <textarea
              rows="1"
              className={!focus ? "form-control shadow-none searchbar searchbar-empty" : "form-control shadow-none searchbar searchbar-full"}
              placeholder="Try the Basel Problem: \sum_{n=1}^{\infty} \frac{1}{n^2}"
              id="MathInput"
              onKeyUp={updatePreview}
              onChange={handleChange}
              onFocus={handleFocus}
              onBlur={handleBlur}
            />
            {!focus ?
              <button onClick={handleClick} className="btn btn-dark" style={{ borderRadius: "0px 30px 30px 0px" }} type="button">Search</button>
              :
              <button onClick={handleClick} className="btn btn-dark" style={{ borderRadius: "0px 30px 00px 0px" }} type="button">Search</button>
            }
          </div>

          {/* Math output preview */}
          <div style={{ position: "relative", paddingTop: 1 }}>
            <div style={{ position: "absolute", width: "100%" }}>
              {!focus ?
                <div className="output" style={{ display: "none" }}>
                  <div id="MathPreview"></div>
                </div>
                :
                <div className="output">
                  <div id="MathPreview"></div>
                </div>
              }
            </div>

          </div>
        </div>
        <div className="w-100 pt-4">
          <input className="form-control" type="file" id="formFile" onChange={handleFileInput} />
          {/* <UploadPDFToS3WithNativeSdk /> */}
          {/* <button onClick={handleClick}>Redirect to results</button> */}
          {/* <button onClick={log_image}>log image!</button> */}
        </div>
      </div>
    </>
  );
}

export default LaTeXInput;
export { get_image };
