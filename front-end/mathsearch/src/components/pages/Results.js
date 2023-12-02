import React, { useState, useEffect } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";
import "./Results.css";
import NavBar from "../NavBar.js";
import { useLocation, useParams } from "react-router-dom";
import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";

import { pdfjs } from 'react-pdf';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.js',
  import.meta.url,
).toString();


/* BEGIN AWS CONSTANTS */

// Constants for Amazon Cognito Identity Pool
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID;
const REGION = process.env.REACT_APP_REGION;
const S3_OUTPUT_BUCKET = process.env.REACT_APP_S3_OUTPUT_BUCKET;

// Initialize the Amazon Cognito credentials provider
AWS.config.region = REGION;
AWS.config.credentials = new CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

/* END AWS CONSTANTS */

const Results = () => {
  /**
   * Grab route params from the URL
   * @param uuid is unique id of the query
   */
  const routeParams = useParams();
  const uuid = routeParams.uuid

  /** Data variables */
  const [pdf, setPdf] = useState(null);
  const [pages, setPages] = useState([]);

  /** Loading variables */
  const [loading, setLoading] = useState(true);
  const [pdfDownloaded, setPdfDownloaded] = useState(false);
  const [jsonDownloaded, setJsonDownloaded] = useState(false);

  const downloadRequest = (uuid) => {
    AWS.config.credentials.get((err) => {
      if (err) {
        console.log("Error retrieving credentials: ", err);
        return;
      }
      const myBucket = new AWS.S3({
        params: { Bucket: S3_OUTPUT_BUCKET },
        region: REGION,
      });

      const fileKey = uuid + ".pdf";
      const jsonKey = uuid + "_results.json";

      console.log(S3_OUTPUT_BUCKET);

      // Download PDF from S3 output bucket
      const pdfParams = {
        Bucket: S3_OUTPUT_BUCKET,
        Key: fileKey,
      };

      myBucket.getObject(pdfParams, (err, data) => {
        if (err) {
          console.error("Error downloading PDF:", err);
        } else {
          // Save the downloaded object to a state variable
          setPdf(data.Body);
          setPdfDownloaded(true);
          console.log("PDF downloaded successfully!");
        }
      });

      // Download json from S3 output bucket
      const jsonParams = {
        Bucket: S3_OUTPUT_BUCKET,
        Key: jsonKey,
      };

      myBucket.getObject(jsonParams, (err, data) => {
        if (err) {
          console.error("Error downloading JSON:", err);
        } else {
          // Save the downloaded object to a state variable
          let json = JSON.parse(data.Body.toString("utf-8"));
          let pages = json.pages;
          setPages(pages);
          setJsonDownloaded(true);
          console.log("JSON downloaded successfully!");
        }
      });
    });
  };

  /** Retrieve the data */
  const fetchData = async () => {
    if (!pdfDownloaded || !jsonDownloaded) {
      console.log(pdfDownloaded);
      console.log(jsonDownloaded);
      // downloadRequest("123456");
      downloadRequest(uuid);
    } else {
      console.log("Loading is complete!")
      setLoading(false);
    }
  };

  // Run useEffect only on page load
  useEffect(() => {
    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, [pdfDownloaded, jsonDownloaded]);

  const handleTestClick = (event) => {
    console.log(uuid)
    console.log(pages);
    console.log(pdf);
    console.log(pdfDownloaded);
    console.log(jsonDownloaded);
  };

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
      pdf.push(
        <Page
          renderAnnotationLayer={false}
          renderTextLayer={false}
          pageNumber={i}
        />
      );
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

  return (
    <>
      {loading ? (
        <div class="page">
          {/* <button onClick={handleTestClick}>Test</button> */}
          <div class="center">
            <div class="loader"></div>
          </div>
        </div>
      ) : (
        <div style={{backgroundColor: "#eeeeee"}}>
          <NavBar />
          {/* <button onClick={handleTestClick}>Test</button> */}
          {pdf !== null && pages && (
            <div>
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
                  <Document
                    file={{ data: pdf }}
                    onLoadSuccess={onDocumentLoadSuccess}
                    onLoadError={console.error}
                  >
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
          )}
        </div>
      )}
    </>
  );
};

export default Results;
