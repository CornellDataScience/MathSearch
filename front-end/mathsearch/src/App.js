import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import NavBar from './NavBar/NavBar.js';
import UploadPDFToS3WithNativeSdk from './UploadPDFToS3WithNativeSdk.js';

function App() {

  console.log(process.env.REACT_APP_API_KEY)

  return (
    <div className="App">
      <NavBar />

      <div className="input-section">
        <h1 className="title">MathSearch</h1>
        <form>
          <input className="text-field" type="text" name="latex" placeholder="Type LaTex here..." />
          {/* <input class="pdf-select" type="file" name="pdf" /> */}
        </form>
        <UploadPDFToS3WithNativeSdk />
      </div>
    </div>
  );
}

export default App;
