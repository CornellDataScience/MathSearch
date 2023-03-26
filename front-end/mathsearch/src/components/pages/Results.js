import React, { useState, useEffect } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";

const Results = () => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  /** Returns an array of <Page> components, one for each page in the PDF */
  const renderPages = () => {
    var pdf = [];
    for (var i = 1; i <= numPages; i++) {
      pdf.push(<Page pageNumber={i} />);
    }
    return pdf;
  };

  /** Scrolls to element scrollToId */
  const scroll = (id) => {
    const target = document.getElementById(id);
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  }

  return (
    <>
      <div style={{ background: "lightgray" }}>
      <button onClick={() => scroll("5")}>Push</button>
        <br />
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Document file="sample.pdf" onLoadSuccess={onDocumentLoadSuccess}>
            {renderPages().map((item, index) => (
              <div id={index + 1}>
                {item}
                <br />
              </div>
            ))}
          </Document>
          <p>
            Page {pageNumber} of {numPages}
          </p>
        </div>
      </div>
      <div id="h">Hello</div>
    </>
  );
};

export default Results;
