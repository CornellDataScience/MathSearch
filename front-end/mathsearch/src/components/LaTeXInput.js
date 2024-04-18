import React, { useState } from "react";
import ReactDOM from "react-dom";
import "katex/dist/katex.min.css";
import { BlockMath, InlineMath } from "react-katex";
import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";
import { v4 } from "uuid";
import { useNavigate } from "react-router-dom";
import "./LaTeXInput.css";
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import { jsPDF } from 'jspdf'
import 'svg2pdf.js';

//import MathInput from './Canvas.js';

function updatePreview() {
  let rawtext = document.getElementById("MathInput").value;
  ReactDOM.render(
    <BlockMath math={rawtext} />,
    document.getElementById("MathPreview")
  );
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
  const [error, setError] = useState({ isError: false, message: "" });



  /** Function to upload SVG as PDF and another PDF file to S3 */
  /** Function to upload SVG as PDF and another PDF file to S3 */
  const uploadRequest = async (file, text) => {
    const s3 = new AWS.S3();
    const fileKey = "inputs/" + uuid + "_pdf";
    const convertedPDFKey = "inputs/" + uuid + "_image";

    try {
      // console.log('S3_INPUT_BUCKET');
      // Fetch SVG from URL
      fetch(`https://math.vercel.app/?from=${text}`, { mode: 'no-cors' })
        .then(response => response.text()) // Get SVG content as text
        .then(svg => {
          //console.log("SVG Data:", svg);  // Check if SVG data looks correct

          const doc = new jsPDF({
            orientation: 'landscape',  // Set orientation to landscape if needed
            unit: 'pt',
            format: 'a4'
          });

          const element = document.createElement('div');  // Create a container for the SVG
          element.innerHTML = svg;  // Insert SVG into the container
          document.body.appendChild(element);  // Append container to body to render SVG

          const svgElement = element.querySelector('svg');  // Get the SVG element
          document.body.removeChild(element);

          const width = svgElement.viewBox.baseVal.width;  // Get original width from SVG
          const height = svgElement.viewBox.baseVal.height;  // Get original height from SVG
          const scaleFactor = 0.5;  // Scale factor for medium size (adjust as needed)

          // Calculate scaled width and height maintaining the aspect ratio
          const scaledWidth = width * scaleFactor;
          const scaledHeight = height * scaleFactor;

          // Generate PDF from the SVG at specified position and size
          doc.svg(svgElement, {
            x: 72,  // X position in the PDF (1 inch from the left)
            y: 72,  // Y position in the PDF (1 inch from the top)
            width: scaledWidth,
            height: scaledHeight,
            loadExternalStyleSheets: true  // Set true to load external styles if your SVG uses them
          })
        }).then((pdfBlob) => {

          //doc.save('blob').then(pdfBlob => {
          // Save the PDF as a Blob
          const convertedPDFParams = {
            ACL: "public-read",
            Body: pdfBlob,
            Bucket: S3_INPUT_BUCKET,
            Key: convertedPDFKey,
          };

          // Upload the converted PDF to S3
          s3.upload(convertedPDFParams, (err, data) => {
            if (err) {
              console.error('Error uploading converted PDF: ', err);
              return;
            }
            console.log('Successfully uploaded converted PDF:', data.Location);
          });
          //})
          //.catch(error => {
          //console.error('Error fetching or converting SVG:', error);
          // });
        })



      // Parameters for existing PDF upload
      const existingPDFParams = {
        ACL: "public-read",
        Body: file,
        Bucket: S3_INPUT_BUCKET,
        Key: fileKey,
      };

      // Upload existing PDF to S3
      s3.upload(existingPDFParams, function (err, data) {
        if (err) {
          console.error('Error uploading existing PDF:', err);
        } else {
          console.log('Successfully uploaded existing PDF:', data.Location);
        }
      });

    } catch (error) {
      console.error('Error in processing or uploading file:', error);
    }
  };

  /** Handles when the user clicks the Search button */
  const handleClick = async () => {
    // Reset the error state at the beginning of each submission attempt
    setError({ isError: false, message: "" });

    // Ensure there's a file selected and the text is not empty before proceeding
    if (!selectedFile) {
      setError({ isError: true, message: "No file selected for upload." });
      return; // Stop execution if no file is selected
    }

    if (text.trim() === "") {
      setError({ isError: true, message: "Text input cannot be empty." });
      return; // Stop execution if text input is empty
    }

    // No need to check for existing errors here as we reset them at the start
    // and we have already checked for all input-related errors above

    // If no errors, proceed with upload
    await uploadRequest(selectedFile, text);

    //await new Promise(resolve => setTimeout(resolve, 2000));

    navigate(`/results/${uuid}`);

    setError({ isError: false, message: "" });
    ;
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

  const handleFileInput = (e) => {
    const file = e.target.files[0];

    // Check if the file is a PDF by looking at its MIME type
    if (file && file.type === "application/pdf") {
      console.log("PDF file selected:", file);
      setSelectedFile(file);
      // Ensure any previous error state is cleared upon successful file selection
      setError({ isError: false, message: "" });
    } else {
      console.log("Invalid file type. Please select a PDF.");
      // Optionally, clear the selected file input if it's not a PDF
      e.target.value = "";
      // And set the selected file in your state to null
      setSelectedFile(null);
      // Update the error state with an appropriate message
      setError({ isError: true, message: "Invalid file type. Please select a PDF." });
    }
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

          <div>
            {/* <MathInput /> */}
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

        {error.isError && (
          <Alert icon={<CheckIcon fontSize="inherit" />} severity="error">
            {error.message}
          </Alert>
        )}



      </div>
    </>
  );
}

export default LaTeXInput;


/** Function to upload SVG as PDF and another PDF file to S3
const uploadRequest = async (file, text) => {
  const s3 = new AWS.S3();
  const fileKey = "inputs/" + uuid + "_pdf";
  const convertedPDFKey = "inputs/" + uuid + "_image";

  // console.log('S3_INPUT_BUCKET');
  // Fetch SVG from URL
  fetch(`/api/latex/?from=${text}`)
    .then(response => response.text()) // Get SVG content as text
    .then(svg => {
      //console.log("SVG Data:", svg);  // Check if SVG data looks correct

      const doc = new jsPDF({
        orientation: 'landscape',  // Set orientation to landscape if needed
        unit: 'pt',
        format: 'a4'
      });

      const element = document.createElement('div');  // Create a container for the SVG
      element.innerHTML = svg;  // Insert SVG into the container
      document.body.appendChild(element);  // Append container to body to render SVG

      const svgElement = element.querySelector('svg');  // Get the SVG element

      if (svgElement) {
        const width = svgElement.viewBox.baseVal.width;  // Get original width from SVG
        const height = svgElement.viewBox.baseVal.height;  // Get original height from SVG
        const scaleFactor = 0.5;  // Scale factor for medium size (adjust as needed)

        // Calculate scaled width and height maintaining the aspect ratio
        const scaledWidth = width * scaleFactor;
        const scaledHeight = height * scaleFactor;

        // Generate PDF from the SVG at specified position and size
        doc.svg(svgElement, {
          x: 72,  // X position in the PDF (1 inch from the left)
          y: 72,  // Y position in the PDF (1 inch from the top)
          width: scaledWidth,
          height: scaledHeight,
          loadExternalStyleSheets: true  // Set true to load external styles if your SVG uses them
        }).then((pdfBlob) => {

          //doc.save('blob').then(pdfBlob => {
          // Save the PDF as a Blob
          const convertedPDFParams = {
            ACL: "public-read",
            Body: pdfBlob,
            Bucket: S3_INPUT_BUCKET,
            Key: convertedPDFKey,
          };

          // Upload the converted PDF to S3
          s3.upload(convertedPDFParams, (err, data) => {
            if (err) {
              console.error('Error uploading converted PDF: ', err);
              return;
            }
            console.log('Successfully uploaded converted PDF:', data.Location);
          });
          //})
          //.catch(error => {
          //console.error('Error fetching or converting SVG:', error);
          // });
          document.body.removeChild(element);
        })

      } else {
        console.error('SVG element not found');
      }
      return
    })

*/