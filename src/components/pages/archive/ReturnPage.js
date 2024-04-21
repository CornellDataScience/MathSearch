import React, { useState } from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack5';
import { useLocation } from 'react-router-dom';

import '../../App.css';
import './ReturnPage.css'

function ReturnPage() {
  const location = useLocation();

  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [listItemsHTML, setListItemsHTML] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    setPageNumber(1);
  }

  function changePage(offset) {
    setPageNumber(prevPageNumber => prevPageNumber + offset);
  }

  function changePageBack() {
    changePage(-1);
  }

  function changePageNext() {
    changePage(+1);
  }

  function gotoPage() {
    let val = parseInt(document.getElementById("gotoPage").value);
    if (val > 0 && val <= numPages) {
      setPageNumber(val);
    } else {
      alert("Page number outside valid range!");
    }
  }

  /* function to display pages */

  function listItems(items) {
    return items.map((items) => <li>{items}</li>)
  }

  async function fetchAsync(url, callback) {
    console.log("polling result");
    let response = await fetch(url);
    console.log("received response.");
    let data = await response.text();
    callback(data);
  }

  function displayResults(response) {
    console.log("response:");

    const tokens = response.split(",");
    const pages = [];
    for (var i = 2; i < tokens.length; i += 6) {
      pages.push(tokens[i]);
    }
    setListItemsHTML(listItems(pages));
    console.log(pages);
  }

  function pollAndDisplayResults() {
    fetchAsync(process.env.REACT_APP_COORD_URL, displayResults);
  }

  return (
    <>
      <div className="return-container">
        <div className="return-content">
          <div>
            {pageNumber > 1 &&
              <button onClick={changePageBack}>Previous Page</button>}
            {pageNumber < numPages &&
              <button onClick={changePageNext}>Next Page</button>}
            <button onClick={gotoPage}>Go To Page</button>
            <input type="number" id="gotoPage"></input>
          </div>
          <p>
            Page {pageNumber} of {numPages}
          </p>
          <div className="results">
            <Document
              file={location.state.selectedFile}
              onLoadSuccess={onDocumentLoadSuccess}
            >
              <Page width={1000} pageNumber={pageNumber} />
            </Document>
            <div className="sidebar">
              <button onClick={pollAndDisplayResults}>Poll Results</button>
              <p>Results on:</p>
              <ol>{listItemsHTML}</ol>
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
