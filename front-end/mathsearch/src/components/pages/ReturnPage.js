import React, { useState } from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack5';


import '../../App.css';
import './ReturnPage.css'

function ReturnPage() {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setPageNumber(1);
  }

  function changePage(offset) {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  }

  function changePageBack(){
    changePage(-1);
  }

  function changePageNext(){
    changePage(+1);
  }

  /* function to display pages */
  const numbers = [1, 2, 3, 4, 5]
  const listItems = numbers.map((number) =>
  <li>Page {number}</li>
);

  return (
    <>
      <div className="return-container">
        <div className="return-content">
          <div>
          {pageNumber > 1 &&
          <button onClick={changePageBack}>Previous Page</button>}
          {pageNumber < numPages &&
          <button onClick={changePageNext}>Next Page</button>}
          </div>
          <p>
            Page {pageNumber} of {numPages}
          </p>
          <div className="results">
            <Document file="./sample.pdf" onLoadSuccess={onDocumentLoadSuccess}>
              <Page pageNumber={pageNumber} />
            </Document>
            <div className="sidebar">
              <p>Results on:</p>
              {/* <ol>
                <li>Page 2</li>
                <li>Page 42</li>
                <li>Page 64</li>
              </ol> */}
              <ol>{listItems}</ol> 
            </div>
          </div>
          <p>
            Page {pageNumber} of {numPages}
          </p>
        </div>
      </div>
    </>
  );
}

export default ReturnPage;
