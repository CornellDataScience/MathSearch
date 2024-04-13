import React, { useState } from 'react';

import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.css';


import '../../App.css';
import './Home.css'

import logo from './logo_white.png'; // Ensure the path is correct relative to this script

// App.js
function App() {
  return (
    <div className="App">
      <header className="App-header">
      </header>
      <body>
        <main className="App-main">


          <div className="mission-section">
            <div className="mission-text">
              <h1>MathSearch</h1>
              <br></br>
              <br></br>
              <p>MathSearch is a service provided by the Cornell Data Science Project Team. It allows users to search for equations in PDFs.</p>

            </div>
            <div className="mission-image">
              <img src={logo} alt="Mission Image" />

            </div>
          </div>
          <section className="problem">
            <div className='problem-left'>
              <h2>Finding Equations in Large Documents Can be Tedious!</h2>
            </div>
            <div className='problem-right'>
              <p>Problem Statement: </p>
              <p> <b>"Ctrl-F" </b> Fails when...</p>
              <ul className='dot-list'>
                <li>Equations use different symbols to represent the same general ideas.</li>
                <li>Equations have symbols not included on the standard keyboard.</li>
              </ul>
              <p>Our Solution: <b>MathSearch!</b></p>
            </div>
          </section>
          <section className='features'>
            <h3>Features</h3>
            <div className='features-content'>
              <div className='step'>
                <h3>STEP 1</h3>
                <br></br>
                <h2>Equation</h2>
                <p>Type the LaTeX equation</p>
              </div>
              <div className='step'>
                <h3>STEP 2</h3>
                <br></br>
                <h2>Upload .pdf</h2>
                <p>Upload the .pdf you want to search</p>
              </div>
              <div className='step'>
                <h3>STEP 3</h3>
                <br></br>
                <h2>Results</h2>
                <p>Find the equations in the document</p>
              </div>
            </div>
          </section>
          <section className="team-section">
            <h2>Our Team</h2>

            <section className="team-section-content">


              <section className="member column">
                <ul className="team-list">
                  <b>Past team members (FA22):</b>
                  <li>Alexander Wang</li>
                  <li>Derek Lee</li>
                  <li>Felix Hohne</li>
                  <li>Kaitlyn Chen</li>
                  <li>Laura Gong</li>
                  <li>Mason Bulling</li>
                  <li>Ronin Sharma</li>
                  <li>Ryan Lee</li>
                  <li>Varun Gande</li>
                  <li>Vivian Chen</li>
                </ul>
              </section>
              <section className="member column">
                <ul className="team-list">
                  <b>Current team members:</b>
                  <li>Andrea Siby</li>
                  <li>Cade Jin</li>
                  <li>Deniz BT</li>
                  <li>Emerald Liu</li>
                  <li>Jason Zheng</li>
                  <li>Jerry Chen</li>
                  <li>Katie Zelvin</li>
                  <li>Pun Chalxanien</li>
                  <li>Travis Zhang</li>
                </ul>
              </section>
              <section className="member column">
                <ul className="team-list">
                  <b>Past team members (SP23):</b>
                  <li>Alice Um</li>
                  <li>Darren Key</li>
                  <li>Johann Lee</li>
                </ul>
              </section>
            </section>

          </section>
        </main>
      </body>
    </div>
  );
}
export default App;