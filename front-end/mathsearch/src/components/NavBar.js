import '../App.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap/dist/css/bootstrap.css';

function NavBar() {
  return (
    <header>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          {/* Navbar brand */}
          <a className="navbar-brand" href="/" style={{ display: "flex" }}>
            <div style={{ display: "flex", alignItems: "center", paddingRight: "0.5rem" }}>
              <img src="/logo2.svg" width="30" height="30" />
            </div>
            <div style={{ display: "flex", alignItems: "center" }}>
              <strong>MathSearch</strong>
            </div>
          </a>

          {/* Responsive toggle */}
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
            aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

          {/* Navbar content */}
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link" href="/">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/about">About</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default NavBar;
