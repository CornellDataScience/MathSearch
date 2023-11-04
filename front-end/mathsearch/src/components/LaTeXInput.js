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

  const handleChange = async (event) => {
    setText(event.target.value)
  }

  return (
    <>
      <div className="latex-input-container">
        <div className="latex-input-content">
          <div className="input">
            <textarea
              rows="1"
              className={text === "" ? "searchbar searchbar-empty" : "searchbar searchbar-full"}
              placeholder="Try the Basel Problem: \sum_{n=1}^{\infty} \frac{1}{n^2}"
              id="MathInput"
              onKeyUp={updatePreview}
              onChange={handleChange}
            >
            </textarea>
          </div>
          {text === "" ?
            <div style={{ visibility: "hidden" }} className="output">
              <div id="MathPreview"></div>
            </div>
            :
            <div className="output">
              <div id="MathPreview"></div>
            </div>
          }
        </div>
        <input className="form-control" type="file" id="formFile" />
        {/* <UploadPDFToS3WithNativeSdk /> */}
        <button onClick={handleClick}>Redirect to results</button>
        {/* <button onClick={log_image}>log image!</button> */}
      </div>
    </>
  );
}

export default LaTeXInput;
export { get_image };
