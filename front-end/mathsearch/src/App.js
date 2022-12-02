// External library imports
import React, {useState} from 'react';

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
import ReturnPage from './components/pages/ReturnPage.js';

// Internal CSS imports
import './App.css';

const [selectedFile, setSelectedFile] = useState(null);

function App() {
   return (
    <>
      <Router>
        <NavBar />
        {/* Add persistent components*/}
        <Routes>
          {/* Add Routes */}
          {/*  <Route exact path='/' element={<Component />} /> */}
          <Route exact path='/' element={<Home />} />
          <Route exact path='/returnpage' element={<ReturnPage />}/>
        </Routes>
      </Router>
    </>
  );
}

export default App;
