import React from 'react';
import ReactDOM from 'react-dom'
import 'katex/dist/katex.min.css';
import { BlockMath, InlineMath } from 'react-katex';

import "./LaTeXInput.css";

function updatePreview() {
   let rawtext = document.getElementById('MathInput').value;
  console.log(rawtext);
   ReactDOM.render(<BlockMath math={rawtext}/>,
                document.getElementById('MathPreview'));
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
      </div>
    </>
  );
}

export default LaTeXInput;
