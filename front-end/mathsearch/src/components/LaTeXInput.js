import React from 'react';
import ReactDOM from 'react-dom'
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';

import "./LaTeXInput.css";

function updatePreview() {
   let rawtext = document.getElementById('MathInput').value;
   ReactDOM.render(<BlockMath math={rawtext}/>,
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

  return (
    <>
      <div className="latex-input-container">
        <div className="latex-input-content">
            <div className="input">
                <textarea
                  placeholder="Try the Basel Problem \sum_{n=1}^{\infty} \frac{1}{n^2}"
                  id="MathInput"
                  onKeyUp={updatePreview}
                  >
                </textarea>
            </div>
            <div className="output">
              <div id="MathPreview"></div>
            </div>
        </div>
        {/* <button onClick={log_image}>log image!</button> */}
      </div>
    </>
  );
}

export default LaTeXInput;
export {get_image};
