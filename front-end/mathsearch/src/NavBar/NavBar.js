import '../App.css';
import 'bootstrap/dist/css/bootstrap.css';

function NavBar() {
  return (
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#"><strong>MathSearch</strong></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">About</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Vision</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Algorithm</a>
            </li>
          </ul>
        </div>
      </nav>
    </header>
  );
}

export default NavBar;