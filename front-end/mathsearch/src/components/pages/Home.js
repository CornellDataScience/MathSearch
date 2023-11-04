import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import NavBar from '../NavBar.js';

import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.css';

import UploadPDFToS3WithNativeSdk from '../UploadPDFToS3WithNativeSdk.js';
import LaTeXInput from '../LaTeXInput.js';
import pdf from "./sample.pdf"

import '../../App.css';
import './Home.css'

function Home() {
  // const [loading, setLoading] = useState(false)
  // const navigate = useNavigate()
  // const redirect = async () => {
  //   // Test code
  //   // try {
  //   const url = "http://mathsearch.org/api/response_pdf";
  //   const response = await fetch(url);
  //   // console.log("COOL")
  //   // console.log(response)
  //   const pdfBinary = await response.blob()

  //   const url2 = "http://mathsearch.org/api/response_pages"
  //   const response2 = await fetch(url2);
  //   const pages = await response2.json()
  //   // console.log(pages)
  //   // const iframe = document.createElement('iframe');
  //   // iframe.src = `https://mozilla.github.io/pdf.js/web/viewer.html?file=${url}`;
  //   // document.body.appendChild(iframe);
  //   // } catch (err) {
  //   //   console.log(err)
  //   // }

  //   // Current code
  //   // const url = "http://mathsearch.org/api/result"
  //   // const response = await fetch(url);
  //   // const json = await response.json();
  //   // console.log("hello")
  //   // console.log(json)
  //   navigate('/results/request_id_here', { state: { pdf: pdfBinary, pages: pages } })
  // }

  // const test_api = async () => {
  //   const url = "http://mathsearch.org/api/test"
  //   const response = await fetch(url);
  //   console.log(await response.text());
  // }

  // const handleClick = async () => {
  //   // setLoading(true)
  //   // await new Promise(resolve => setTimeout(resolve, 5000));
  //   // redirect()

  //   // Send an API request with uploaded PDF blob
  //   // Current request is a placeholder, replace with something else later
  //   // const url = "http://mathsearch.org/api/send_request"
  //   // const response = await fetch(url);

  //   // Navigate to results page to wait for result
  //   navigate('/results/request_id_here')
  //   // test_api()
  // }

  return (
    <>
      <NavBar />
      <div className="home-container">
        <div className="home-content">
          <h1 className="title">MathSearch</h1>
          <LaTeXInput />
        </div>
      </div >
    </>
  );
}

export default Home;
