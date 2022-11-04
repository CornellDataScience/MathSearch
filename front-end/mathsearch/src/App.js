// External library imports
import React from 'react';

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

// Internal CSS imports
import './App.css';


function App() {
  ////////////////////////////////////////////////////////////////////////////////////////////////////////
  // return (                                                                                           //
  //   <div className="App">                                                                            //
  //     <NavBar />                                                                                     //
  //                                                                                                    //
  //     <div className="input-section">                                                                //
  //       <h1 className="title">MathSearch</h1>                                                        //
  //       <form>                                                                                       //
  //         <input className="text-field" type="text" name="latex" placeholder="Type LaTex here..." /> //
  //         {/* <input class="pdf-select" type="file" name="pdf" /> */}                                //
  //       </form>                                                                                      //
  //       <UploadPDFToS3WithNativeSdk />                                                               //
  //     </div>                                                                                         //
  //   </div>                                                                                           //
  // );                                                                                                 //
  ////////////////////////////////////////////////////////////////////////////////////////////////////////

   return (
    <>
      <Router>
        <NavBar />
        {/* Add persistent components*/}
        <Routes>
          {/* Add Routes */}
          {/*  <Route exact path='/' element={<Component />} /> */}
          <Route exact path='/' element={<Home />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
