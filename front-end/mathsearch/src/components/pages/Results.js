import React, { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf/dist/esm/entry.webpack5";
import "./Results.css";
import NavBar from "../NavBar.js";
import { useLocation, useParams } from "react-router-dom";
import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";
// import { pdfjs } from 'react-pdf';

// pdfjs.GlobalWorkerOptions.workerSrc = new URL(
//   'pdfjs-dist/build/pdf.worker.min.js',
//   import.meta.url,
// ).toString();

const url = `//cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`
pdfjs.GlobalWorkerOptions.workerSrc = url


/* BEGIN AWS CONSTANTS */

// Constants for Amazon Cognito Identity Pool
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID;
const REGION = process.env.REACT_APP_REGION;
const S3_OUTPUT_BUCKET = process.env.REACT_APP_S3_OUTPUT_BUCKET;
const WEBSOCKET_URL = 'wss://t05sr0quhf.execute-api.us-east-1.amazonaws.com/production/';

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

  const [webSocket, setWebSocket] = useState(null);

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
      // const fileKey = "6c5f1f35-bba5-4346-a04f-485b8fd167d6.pdf";
      const jsonKey = uuid + "_results.json";
      // const jsonKey = "6c5f1f35-bba5-4346-a04f-485b8fd167d6" + "_results.json";

      console.log(S3_OUTPUT_BUCKET);

      // Download PDF from S3 output bucket
      console.log(fileKey)
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


  useEffect(() => {
    console.log("Component mounted, setting up WebSocket");
    const ws = new WebSocket(`${WEBSOCKET_URL}?uuid=${uuid}`);

    ws.onopen = () => {
      console.log('WebSocket Connected');
      const message = JSON.stringify({ action: "register", uuid: uuid });
      console.log('Sending message:', message);
      ws.send(message);
    };

    ws.onmessage = (event) => {
      console.log('WebSocket Message:', event.data);
      // Handle incoming messages
      // Assuming 'message' has a 'type' property to dictate actions
      console.log('Start Fetch')
      const message = JSON.parse(event.data);
      if (message.type === "PDF_PROCESSING_COMPLETE") {
        console.log("Results are ready:", message.message);
        fetchData();
      }
    };

    ws.onerror = (error) => {
      console.log('WebSocket Error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket Disconnected');
    };

    setWebSocket(ws);

    // This function might need to be moved outside useEffect or wrapped in a useCallback if used elsewhere
    const fetchData = async () => {
      if (!pdfDownloaded || !jsonDownloaded) {
        console.log(pdfDownloaded);
        console.log(jsonDownloaded);
        downloadRequest(uuid);
      }
      setLoading(false);
    };

    // Clean up on unmount
    return () => {
      ws.close();
    };
  }, [pdfDownloaded, jsonDownloaded]); // Keep these dependencies if their changes should affect the effect



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
        <div style={{ backgroundColor: "#eeeeee" }}>
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