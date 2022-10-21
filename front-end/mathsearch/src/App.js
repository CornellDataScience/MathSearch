import './App.css';
import 'bootstrap/dist/css/bootstrap.css';
import NavBar from './NavBar/NavBar.js';
import UploadPDFToS3WithNativeSdk from './UploadPDFToS3WithNativeSdk.js';

function App() {
  return (
    <div className="App">
      <NavBar />

      <div class="input-section">
        <h1 class="title">MathSearch</h1>
        <form>
          <input class="text-field" type="text" name="latex" placeholder="Type LaTex here..." />
          {/* <input class="pdf-select" type="file" name="pdf" /> */}
        </form>
        <UploadPDFToS3WithNativeSdk />
      </div>
    </div>
  );
}

export default App;
