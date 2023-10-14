import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import NavBar from '../NavBar.js';

import UploadPDFToS3WithNativeSdk from '../UploadPDFToS3WithNativeSdk.js';
import LaTeXInput from '../LaTeXInput.js';
import pdf from "./sample.pdf"

import '../../App.css';
import './Home.css'

function Home() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const redirect = async () => {
    // Test code
    // try {
    const url = "http://mathsearch.org/api/response_pdf";
    const response = await fetch(url);
    const pdfBinary = await response.blob()

    const url2 = "http://mathsearch.org/api/response_pages"
    const response2 = await fetch(url2);
    const pages = await response2.json()
    // console.log(pages)
    // const iframe = document.createElement('iframe');
    // iframe.src = `https://mozilla.github.io/pdf.js/web/viewer.html?file=${url}`;
    // document.body.appendChild(iframe);
    // } catch (err) {
    //   console.log(err)
    // }

    // Current code
    // const url = "http://mathsearch.org/api/result"
    // const response = await fetch(url);
    // const json = await response.json();
    // console.log("hello")
    // console.log(json)
    navigate('/results', { state: { pdf: pdfBinary, pages: pages } })
  }

  const test_api = async () => {
    const url = "http://mathsearch.org/api/test"
    const response = await fetch(url);
    console.log(await response.text());
  }

  const handleClick = async () => {
    setLoading(true)
    await new Promise(resolve => setTimeout(resolve, 5000));
    redirect()
    // test_api()
  }

  return (
    <>
      {loading ?
        <div class="page">
          <div class="center">
            <div class="loader"></div>
          </div>

        </div>
        :
        <div>
          <NavBar />
          <div className="home-container">
            <div className="home-content">
              <h1 className="title">MathSearch</h1>
              <LaTeXInput />
              {/* <UploadPDFToS3WithNativeSdk /> */}
              <button onClick={handleClick}>Redirect to results</button>
            </div>
          </div>
        </div>
      }
    </>
  );
}

export default Home;
