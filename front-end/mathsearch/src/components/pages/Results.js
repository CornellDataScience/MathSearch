import React, { useState, useEffect } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";
import "./Results.css";
import NavBar from '../NavBar.js';
import { useLocation, useParams } from 'react-router-dom';

const Results = () => {
  // /**
  //   * All state data passed into this window and must include at least
  //   * the following:
  //   * @param pdf is the pdf to render
  //   * @param pages is the list of page numbers
  //   */

  // const data = useLocation().state

  /** Data variable */
  const [data, setData] = useState(null)

  /** Loading variable */
  const [loading, setLoading] = useState(true)

  /**
   * Retrieve the data
   */
  const fetchData = async () => {
    const url = "http://mathsearch.org/api/response_pdf";
    const response = await fetch(url);

    const pdfBinary = await response.blob()

    const url2 = "http://mathsearch.org/api/response_pages"
    const response2 = await fetch(url2);
    const pages = await response2.json()


    await new Promise(resolve => setTimeout(resolve, 5000));
    setLoading(false)

    return { pdf: pdfBinary, pages: pages }
  }

  // Run useEffect only on page load
  useEffect(() => {
    const func = async () => {
      setData(await fetchData())
    }
    func()
  }, [])

  /**
   * request id is passed from the url
   */
  const { requestId } = useParams();

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

  // Temporary hardcoding
  // let pdf_file = data.pdf
  // let pages = data.pages
  // console.log(data.pdf, data.pages)

  return (
    <>
      {loading ?
        <div class="page">
          <div class="center">
            <div class="loader"></div>
          </div>
        </div>
        :
        <>
          <NavBar />
          {
            (data.pdf && data.pages) &&
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
                  <Document file={data.pdf} onLoadSuccess={onDocumentLoadSuccess} onLoadError={console.error}>
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
                    {data.pages.map((item, index) => (
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
          }
        </>
      }
    </>
  );
};

export default Results;
