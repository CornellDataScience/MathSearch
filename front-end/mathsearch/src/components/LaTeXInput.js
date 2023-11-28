import React, { useState } from "react";
import ReactDOM from "react-dom";
import "katex/dist/katex.min.css";
import { BlockMath, InlineMath } from "react-katex";
import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";
import { v4 } from "uuid";
import { useNavigate } from "react-router-dom";
import "./LaTeXInput.css";

function updatePreview() {
  let rawtext = document.getElementById("MathInput").value;
  ReactDOM.render(
    <BlockMath math={rawtext} />,
    document.getElementById("MathPreview")
  );
}

function get_image() {
  var tex = document.getElementById("MathInput").value;
  var url =
    "http://chart.apis.google.com/chart?&cht=tx&chl=" +
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
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID;
const REGION = process.env.REACT_APP_REGION;
const S3_INPUT_BUCKET = process.env.REACT_APP_S3_INPUT_BUCKET;

// Initialize the Amazon Cognito credentials provider
AWS.config.region = REGION;
AWS.config.credentials = new CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

/* END AWS CONSTANTS */

function LaTeXInput() {
  const navigate = useNavigate();
  const uuid = v4();

  const [text, setText] = useState("");
  const [focus, setFocus] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [progress, setProgress] = useState(0);

  /** Convert some text to a url which is an image */
  const convert_text_to_image_url = (text) => {
    var url =
      "http://chart.apis.google.com/chart?&cht=tx&chl=" +
      encodeURIComponent(text) +
      "&chof=png";
    return url;
  };

  /** Uploads a PDF file and text query to S3 */
  const uploadRequest = (file, text) => {
    AWS.config.credentials.get((err) => {
      if (err) {
        console.log("Error retrieving credentials: ", err);
        return;
      }

      const myBucket = new AWS.S3({
        params: { Bucket: S3_INPUT_BUCKET },
        region: REGION,
      });

      const fileKey = "inputs/" + uuid + "_pdf";
      const imageKey = "inputs/" + uuid + "_image";
      const imageURL = convert_text_to_image_url(text);

      console.log(S3_INPUT_BUCKET);

      // Fetch image and upload to S3 input bucket
      fetch(imageURL)
        .then((response) => response.blob())
        .then((blob) => {
          const imageParams = {
            ACL: "public-read",
            Body: blob,
            Bucket: S3_INPUT_BUCKET,
            Key: imageKey,
          };

          myBucket
            .putObject(imageParams)
            .on("httpUploadProgress", (evt) => {
              setProgress(Math.round((evt.loaded / evt.total) * 100));
            })
            .send((err) => {
              if (err) console.log(err);
            });
        })

        // Upload PDF to S3 input bucket
        .then(() => {
          const pdfParams = {
            ACL: "public-read",
            Body: file,
            Bucket: S3_INPUT_BUCKET,
            Key: fileKey,
          };

          myBucket
            .putObject(pdfParams)
            .on("httpUploadProgress", (evt) => {
              setProgress(Math.round((evt.loaded / evt.total) * 100));
            })
            .send((err) => {
              if (err) console.log(err);
            });
        });
    });
  };

  /** Handles when the user clicks the Search button */
  const handleClick = async () => {
    uploadRequest(selectedFile, text);
    navigate(`/results/${uuid}`, { state: { uuid: uuid } })
  };

  /** Handles when user types in the search bar */
  const handleChange = async (event) => {
    setText(event.target.value);
  };

  /** When user clicks into the search bar */
  const handleFocus = async (event) => {
    setFocus(true);
  };

  /** When user clicks out of the search bar */
  const handleBlur = async (event) => {
    setFocus(false);
  };

  /** When user uploads a file */
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
              className={
                !focus
                  ? "form-control shadow-none searchbar searchbar-empty"
                  : "form-control shadow-none searchbar searchbar-full"
              }
              placeholder="Try the Basel Problem: \sum_{n=1}^{\infty} \frac{1}{n^2}"
              id="MathInput"
              onKeyUp={updatePreview}
              onChange={handleChange}
              onFocus={handleFocus}
              onBlur={handleBlur}
            />
            {!focus ? (
              <button
                onClick={handleClick}
                className="btn btn-dark"
                style={{ borderRadius: "0px 30px 30px 0px" }}
                type="button"
              >
                Search
              </button>
            ) : (
              <button
                onClick={handleClick}
                className="btn btn-dark"
                style={{ borderRadius: "0px 30px 00px 0px" }}
                type="button"
              >
                Search
              </button>
            )}
          </div>

          {/* Math output preview */}
          <div style={{ position: "relative", paddingTop: 1 }}>
            <div style={{ position: "absolute", width: "100%" }}>
              {!focus ? (
                <div className="output" style={{ display: "none" }}>
                  <div id="MathPreview"></div>
                </div>
              ) : (
                <div className="output">
                  <div id="MathPreview"></div>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="w-100 pt-4">
          <input
            className="form-control"
            type="file"
            id="formFile"
            onChange={handleFileInput}
          />
        </div>
      </div>
    </>
  );
}

export default LaTeXInput;
export { get_image };
