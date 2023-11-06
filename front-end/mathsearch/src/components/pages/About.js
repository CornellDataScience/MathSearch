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
                    Hello
                </div>
            </div>
        </>
    );
}

export default About;
