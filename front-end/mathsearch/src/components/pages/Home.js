import React, {useState} from 'react';
import { useNavigate } from "react-router-dom";

import UploadPDFToS3WithNativeSdk from '../UploadPDFToS3WithNativeSdk.js';
import LaTeXInput from '../LaTeXInput.js';
import pdf from "./sample.pdf"

import '../../App.css';
import './Home.css'

function Home() {
  const navigate = useNavigate()
  const redirect = async () => {
    // Test code
    // try {
    const url = "http://mathsearch.org/api/responsetest";
    const response = await fetch(url);
    const pdfBinary = await response.blob()
    const iframe = document.createElement('iframe');
    iframe.src = `https://mozilla.github.io/pdf.js/web/viewer.html?file=${url}`;
    document.body.appendChild(iframe);
    // } catch (err) {
    //   console.log(err)
    // }

    // Current code
    // const url = "http://mathsearch.org/api/result"
    // const response = await fetch(url);
    // const json = await response.json();
    // console.log("hello")
    // console.log(json)
    navigate('/results',{state:{pdf:pdfBinary, pages:[1, 2, 3]}})
  }

  const test_api = async () => {
    const url = "http://mathsearch.org/api/test"
    const response = await fetch(url);
    console.log(await response.text());
  }

  const handleClick = () => {
    redirect()
    // test_api()
  }

  return (
    <>
      <div className="home-container">
        <div className="home-content">
          <h1 className="title">MathSearch</h1>
          <LaTeXInput/>
          <UploadPDFToS3WithNativeSdk />
          <button onClick={handleClick}>Redirect to results</button>
        </div>
      </div>
    </>
  );
}

export default Home;
