import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import NavBar from '../NavBar.js';

import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.css';

import '../../App.css';
import './Home.css'

function About() {
    return (
        <>
            <div style={{ backgroundColor: "#eeeeee", minHeight: "100vh" }}>
                <NavBar />
                <div className="home-container">
                    <p>Current team members:</p>
                    <ul>
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
                    <p>Past team members: (SP23)</p>
                    <ul>
                        <li>Alice Um</li>
                        <li>Darren Key</li>
                        <li>Johann Lee</li>
                    </ul>
                    <p>Past team members: (FA22)</p>
                    <ul>
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
                </div>
            </div>
        </>
    );
}

export default About;
