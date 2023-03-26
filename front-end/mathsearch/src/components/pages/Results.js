import React, { useState, useEffect } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";
import "./Results.css";

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
  };

  /** index : value = result item : page number */
  const pages = [1, 3, 5, 7, 51];

  return (
    <>
      <div style={{ background: "lightgray" }}>
        <br />
        <div className="grid-container">
          {/* Empty column */}
          <div></div>

          {/* PDF */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              height: "90vh",
              overflow: "scroll",
            }}
          >
            <Document file="sample.pdf" onLoadSuccess={onDocumentLoadSuccess}>
              {renderPages().map((item, index) => (
                <div id={index + 1}>
                  {item}
                  <br />
                </div>
              ))}
            </Document>
          </div>

          {/* Nav buttons */}
          <div
            style={{
              background: "white",
              borderRadius: "1em",
              display: "flex",
              justifyContent: "center",
            }}
          >
            <div style={{ padding: "1em" }}>
              <div style={{ textAlign: "center", paddingBottom: "2em" }}>
                <b>Results</b>
              </div>
              {pages.map((item, index) => (
                <div>
                  <button className="button" onClick={() => scroll(item)}>
                    Page {item}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Results;
