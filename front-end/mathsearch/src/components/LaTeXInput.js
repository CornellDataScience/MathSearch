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



function LaTeXInput() {
  const navigate = useNavigate()

  const [text, setText] = useState("")
  const [focus, setFocus] = useState(false)

  const handleClick = async () => {
    // setLoading(true)
    // await new Promise(resolve => setTimeout(resolve, 5000));
    // redirect()

    // Send an API request with uploaded PDF blob
    // Current request is a placeholder, replace with something else later
    // const url = "http://mathsearch.org/api/send_request"
    // const response = await fetch(url);

    // Navigate to results page to wait for result
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

  return (
    <>
      <div className="latex-input-container">
        <div className="latex-input-content">
          <div className="input">
            <textarea
              rows="1"
              className={!focus ? "searchbar searchbar-empty" : "searchbar searchbar-full"}
              placeholder="Try the Basel Problem: \sum_{n=1}^{\infty} \frac{1}{n^2}"
              id="MathInput"
              onKeyUp={updatePreview}
              onChange={handleChange}
              onFocus={handleFocus}
              onBlur={handleBlur}
            />
          </div>
          <div style={{ position: "relative" }}>
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
          <input className="form-control" type="file" id="formFile" />
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
