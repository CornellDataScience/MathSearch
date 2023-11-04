// External library imports
import React, { useState } from 'react';

import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom';

// External CSS imports
import 'bootstrap/dist/css/bootstrap.css';

// Internal component imports
import NavBar from './components/NavBar.js';
import Home from './components/pages/Home.js';
// import ReturnPage from './components/pages/ReturnPage.js';
import Results from './components/pages/Results.js';

// Internal CSS imports
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  return (
    <>
      <Router>
        {/* Add persistent components*/}
        <Routes>
          {/* Add Routes */}
          {/*  <Route exact path='/' element={<Component />} /> */}
          <Route exact path='/' element={<Home />} />
          {/* <Route exact path='/returnpage' element={<ReturnPage selectedFile={selectedFile} />} /> */}
          <Route path='/results/:requestid' element={<Results />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
