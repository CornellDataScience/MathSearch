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
    const url = "http://mathsearch.org/api/result"
    const response = await fetch(url);
    const json = await response.json();
    // console.log("hello")
    // console.log(json)
    navigate('/results',{state:{pdf:pdf, pages:[1, 2, 3]}})
  }

  const handleClick = () => {
    redirect()
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
