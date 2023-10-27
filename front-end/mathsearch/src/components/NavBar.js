import '../App.css';
import 'bootstrap/dist/css/bootstrap.css';

function NavBar() {
  return (
    <header>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="/" style={{ paddingLeft: "1rem", display: "flex" }}>
          <div style={{ display: "flex", alignItems: "center", paddingRight: "0.5rem" }}>
            <img src="/logo2.svg" width="30" height="30" />
          </div>
          <div style={{ display: "flex", alignItems: "center" }}>
            <strong>MathSearch</strong>
          </div>
        </a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item active">
              <a className="nav-link" href="/">Home</a>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
}

export default NavBar;
