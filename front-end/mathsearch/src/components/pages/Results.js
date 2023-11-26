import React, { useState, useEffect } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack5";
// import "react-pdf/dist/esm/Page/TextLayer.css";
import "./Results.css";
import NavBar from "../NavBar.js";
import { useLocation, useParams } from "react-router-dom";

import { CognitoIdentityCredentials } from "aws-sdk/global";
import AWS from "aws-sdk";
import { v4 } from "uuid";


import hardcoded_pdf from "./asdf.pdf"

/* BEGIN AWS CONSTANTS */

// Constants for Amazon Cognito Identity Pool
const IDENTITY_POOL_ID = process.env.REACT_APP_IDENTITY_POOL_ID;
const REGION = process.env.REACT_APP_REGION;
// const S3_OUTPUT_BUCKET = process.env.REACT_APP_S3_INPUT_BUCKET;
const S3_OUTPUT_BUCKET = "mathsearch-outputs";

AWS.config.region = REGION;

// Initialize the Amazon Cognito credentials provider
AWS.config.credentials = new CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

/* END AWS CONSTANTS */

const Results = () => {
  // /**
  //   * All state data passed into this window and must include at least
  //   * the following:
  //   * @param pdf is the pdf to render
  //   * @param pages is the list of page numbers
  //   */

  // const data = useLocation().state

  /** Data variable */
  // const [data, setData] = useState(null);

  /** Data variables */
  const [pdf, setPdf] = useState(null)
  const [pages, setPages] = useState([])

  /** Loading variable */
  const [loading, setLoading] = useState(true);

  const downloadRequest = (uuidKey) => {
    AWS.config.credentials.get((err) => {
      if (err) {
        console.log("Error retrieving credentials: ", err);
        return;
      }
      const myBucket = new AWS.S3({
        params: { Bucket: S3_OUTPUT_BUCKET },
        region: REGION,
      });

      const fileKey = uuidKey + "_pdf";
      // const imageKey = uuidKey + "_image";
      // const imageURL = convert_text_to_image_url(text);

      console.log(S3_OUTPUT_BUCKET);
      // Fetch image and download from S3 outputs bucket

      // const imageParams = {
      //   ACL: "public-read",
      //   Body: blob,
      //   Bucket: S3_OUTPUT_BUCKET,
      //   Key: imageKey,
      // };

      // myBucket.getObject(imageParams, (err, data) => {
      //   if (err) {
      //     console.error("Error downloading object:", err);
      //   } else {
      //     // Save the downloaded object to a local file
      //     set
      //     console.log("Object downloaded successfully!");
      //   }
      // });

      // myBucket.getObject(imageParams)
      //   .on("httpUploadProgress", (evt) => {
      //     setProgress(Math.round((evt.loaded / evt.total) * 100));
      //   })
      //   .send((err) => {
      //     if (err) console.log(err);
      //   });

      // Download PDF from S3 input bucket
      const pdfParams = {
        Bucket: S3_OUTPUT_BUCKET,
        Key: fileKey,
      };

      myBucket.getObject(pdfParams, (err, data) => {
        if (err) {
          console.error("Error downloading object:", err);
        } else {
          // Save the downloaded object to a state variable
          setPdf(data.Body)
          setPages([1,2,3,4,5,6])
          console.log("Object downloaded successfully!");
          // console.log(hardcoded_pdf)
        }
      });

      // myBucket
      //   .getObject(pdfParams)
      //   .on("httpUploadProgress", (evt) => {
      //     setProgress(Math.round((evt.loaded / evt.total) * 100));
      //   })
      //   .send((err) => {
      //     if (err) console.log(err);
      //   });
    });
  };

  /**
   * Retrieve the data
   */
  const fetchData = async () => {
    // const url = "http://mathsearch.org/api/response_pdf";
    // const response = await fetch(url);

    // const pdfBinary = await response.blob()

    // const url2 = "http://mathsearch.org/api/response_pages"
    // const response2 = await fetch(url2);
    // const pages = await response2.json()

    // Harcode wait 5 seconds
    downloadRequest("12345")
    await new Promise((resolve) => setTimeout(resolve, 5000));
    setLoading(false);

    // return { pdf: pdfBinary, pages: pages };
  };

  // Run useEffect only on page load
  useEffect(() => {
    const func = async () => {
      // setData(await fetchData());
      await fetchData("12345")
    };
    func();
  }, []);

  const handleTestClick = (event) => {
    console.log(pages)
    console.log(pdf)
  }

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
      pdf.push(<Page renderAnnotationLayer={false} renderTextLayer={false} pageNumber={i} />);
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
      {loading ? (
        <div class="page">
          <div class="center">
            <div class="loader"></div>
          </div>
        </div>
      ) : (
        <>
          <NavBar />
          <button onClick={handleTestClick}>Test</button>
          {pdf !== null && pages && (
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
        </>
      )}
    </>
  );
};

export default Results;
