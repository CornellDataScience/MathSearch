import React, { useState } from "react";
import ReactDOM from "react-dom";
import "katex/dist/katex.min.css";
import { BlockMath } from "react-katex";
import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";
import { v4 } from "uuid";
import { useNavigate } from "react-router-dom";
import "./LaTeXInput.css";
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import MathKeyboard from './MathKeyboard';



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
  const [error, setError] = useState({ isError: false, message: "" });

  const [showKeyboard, setShowKeyboard] = useState(false);

  const handleSymbolSelect = (latex) => {
    // Get a reference to the MathInput textarea
    const inputArea = document.getElementById('MathInput');
    const cursorPosition = inputArea.selectionStart;

    setText((prevText) => {
      // Insert the LaTeX at the current cursor position
      const newText =
        prevText.slice(0, cursorPosition) +
        latex +
        prevText.slice(cursorPosition);

      // Determine the position to set the cursor after inserting the LaTeX
      const positions = [latex.indexOf('}'), latex.indexOf(')'), latex.indexOf(']')];
      const validPositions = positions.map(pos => (pos === -1 ? latex.length : pos));
      const firstClosingCharIndex = Math.min(...validPositions) + cursorPosition;

      updatePreview();

      // Set the cursor position after the preview is updated
      setTimeout(() => {
        if (inputArea) {
          inputArea.focus();
          // Place the cursor before the first closing character
          inputArea.setSelectionRange(firstClosingCharIndex, firstClosingCharIndex);
        }
      }, 0);

      return newText;
    });
  };




  const fetch = require('node-fetch');

  const updatePreview = () => {
    const previewElem = document.getElementById("MathPreview");
    if (previewElem) {
      ReactDOM.render(<BlockMath math={text} />, previewElem);
    }
  };


  function cleanSVG(svgData) {
    const svgStart = svgData.indexOf('<svg');
    return svgStart > 0 ? svgData.substring(svgStart) : svgData;
  }

  function extractViewBox(svgString) {
    const viewBoxMatch = svgString.match(/viewBox="([^"]+)"/);
    return viewBoxMatch ? viewBoxMatch[1].split(' ').map(Number) : null;
  }

  function scaleCanvas(svgString, targetWidth) {
    const viewBox = extractViewBox(svgString);
    if (!viewBox) {
      console.error('No viewBox found in SVG');
      return { width: targetWidth, height: 200 }; // Default if no viewBox is present
    }

    const [minX, minY, width, height] = viewBox;
    const aspectRatio = width / height;

    // Calculate the new height based on the target width and the aspect ratio
    const scaledHeight = targetWidth / aspectRatio;

    return { width: targetWidth, height: scaledHeight };
  }


  async function renderLatexToBlob(latexString) {
    const encodedLatexString = encodeURIComponent(latexString);
    const apiUrl = `https://math.vercel.app/?from=${encodedLatexString}`;
    const url = `https://corsproxy.io/?${encodeURIComponent(apiUrl)}`;
    const response = await fetch(url);

    const svgData = await response.text();

    return new Promise((resolve, reject) => {
      const cleanedSVG = cleanSVG(svgData); // Ensure your SVG is properly cleaned
      const dimensions = scaleCanvas(cleanedSVG, 800);
      const canvas = document.createElement('canvas');
      canvas.width = dimensions.width;
      canvas.height = dimensions.height;
      const ctx = canvas.getContext('2d');

      const img = new Image();
      img.onload = () => {
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob((blob) => {
          resolve(blob);  // Now you have a blob that can be uploaded to S3
        }, 'image/png');
      };
      img.onerror = (err) => {
        reject(new Error('Image loading failed: ' + err));
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(cleanedSVG)));
    });
  }


  /** Function to upload SVG as PDF and another PDF file to S3 */
  const uploadRequest = async (file, text) => {
    const s3 = new AWS.S3();
    const fileKey = "inputs/" + uuid + "_pdf";
    const convertedPDFKey = "inputs/" + uuid + "_image";

    const imageBuffer = await renderLatexToBlob(text);


    const convertedPDFParams = {
      ACL: "public-read",
      Body: imageBuffer,
      Bucket: S3_INPUT_BUCKET,
      Key: convertedPDFKey,
    };

    // Upload the converted PDF to S3
    s3.upload(convertedPDFParams, (err, data) => {
      if (err) {
        console.error('Error uploading converted PDF: ', err);
        return;
      }
      //console.log('Successfully uploaded converted PDF:', data.Location);
    });


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
    setShowKeyboard(true);
  };

  /** When user clicks out of the search bar */
  const handleBlur = async (event) => {
    setFocus(false);
    setShowKeyboard(false);
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
        {/* Start of latex-input-content */}
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
              placeholder="Try the Base Problem: \sum_{n=1}^{\infty} \frac{1}{n^2}"
              id="MathInput"
              onKeyUp={updatePreview}
              value={text}
              onChange={handleChange}
              onFocus={handleFocus}
              onBlur={handleBlur}
            />
            <button
              onClick={handleClick}
              className="btn btn-dark"
              style={{ borderRadius: !focus ? "0px 30px 30px 0px" : "0px 30px 0px 0px" }}
              type="button"
            >
              Search
            </button>
          </div>
          {/* Render the MathKeyboard here */}
          <MathKeyboard onSymbolSelect={handleSymbolSelect} isVisible={showKeyboard} />
        </div >
        {/* End of latex-input-content */}

        {/* Math output preview */}
        <div className="output" id="MathPreview" style={{ display: !focus ? "none" : "block" }}>
          {/* MathPreview content will be rendered here */}
        </div>

        {/* File upload input */}
        <div style={{ marginTop: '20px' }} className="file-upload-container">
          <input
            className="form-control"
            type="file"
            id="formFile"
            onChange={handleFileInput}
          />
        </div>

        {/* Error message */}
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
