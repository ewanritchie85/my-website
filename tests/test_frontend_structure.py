from pathlib import Path
import re
import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

def _soup(name):
    p = ROOT / name
    assert p.exists(), f"{name} missing"
    return BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")

def test_html_files_exist():
    for f in ["index.html", "projects.html", "certificates.html", "navbar.html"]:
        assert (ROOT / f).exists()

def test_css_js_dirs_exist():
    assert (ROOT / "css" / "style.css").exists()
    for js in ["functions.js", "load-navbar.js", "spotify-now-playing.js", "turbo-death-warrior.js"]:
        assert (ROOT / "js" / js).exists(), f"js/{js} missing"

def test_index_asset_refs():
    html = (ROOT / "index.html").read_text()
    assert 'href="css/style.css"' in html
    assert 'src="js/functions.js"' in html
    assert 'src="js/load-navbar.js"' in html
    assert 'style.css"' not in html.replace('css/style.css', '')  # no stray root css
    soup = _soup("index.html")
    assert soup.title and "About Me" in soup.title.text

def test_projects_asset_refs():
    html = (ROOT / "projects.html").read_text()
    assert 'href="css/style.css"' in html
    assert 'src="js/functions.js"' in html
    assert 'src="js/load-navbar.js"' in html
    assert 'src="js/spotify-now-playing.js' in html
    assert 'src="js/turbo-death-warrior.js"' in html

def test_certificates_asset_refs():
    html = (ROOT / "certificates.html").read_text()
    assert 'href="css/style.css"' in html
    assert 'src="js/functions.js"' in html

def test_projects_has_11_projects():
    soup = _soup("projects.html")
    lis = soup.select(".project-list li")
    assert len(lis) == 11, f"expected 11, got {len(lis)}"
    expected = {"nikitai","spotify-api","notebook-data-refresher","metoffice-etl","word-wheel-solver","turbo-death-warrior","task-manager-app","my-portfolio-website","ten10-platform","ten10-core","northcoders"}
    got = {li.get("data-project") for li in lis}
    assert got == expected, f"mismatch {got}"

def test_project_containers():
    soup = _soup("projects.html")
    for pid in ["nikitai","spotify-api","turbo-death-warrior"]:
        assert soup.find(id=pid) is not None, f"missing project #{pid}"

def test_navbar_structure():
    soup = _soup("navbar.html")
    assert soup.find(class_="navbar")
    assert soup.find(id="mug-shot")
    btns = [b.text.strip() for b in soup.select(".buttons")]
    assert btns == ["About Me","Projects","Certificates"]

def test_certificates_images():
    soup = _soup("certificates.html")
    imgs = soup.select(".certs-row img")
    assert len(imgs) >= 10
    for img in imgs:
        src = img.get("src","")
        assert src.startswith("./images/certs/") or src.startswith("images/certs/")

def test_images_exist():
    # spot check critical images
    for rel in ["images/mug-shot.png", "images/logos/python-logo.webp", "images/logos/github-logo.png", "images/metoffice_infra.png"]:
        assert (ROOT / rel).exists(), f"{rel} missing"

def test_css_contains_key_selectors():
    css = (ROOT / "css" / "style.css").read_text()
    for sel in [".navbar", ".page-content", ".project-list", "#mug-shot", "#tdw-game"]:
        assert sel in css, f"{sel} not in css"

def test_js_contains_expected_functions():
    # functions.js
    f = (ROOT / "js" / "functions.js").read_text()
    assert "loadSpotifyExperience" in f or "spotify" in f.lower()
    assert "word-wheel-form" in f

    lb = (ROOT / "js" / "load-navbar.js").read_text()
    assert "fetch('navbar.html')" in lb or 'fetch("navbar.html")' in lb or "navbar.html" in lb

    sp = (ROOT / "js" / "spotify-now-playing.js").read_text()
    assert "function renderArtists" in sp
    assert "function loadSpotifyExperience" in sp
    assert "/spotify-info" in sp

    tdw = (ROOT / "js" / "turbo-death-warrior.js").read_text()
    assert "initTurboDeathWarrior" in tdw
    assert "TDW_API_BASE" in tdw
    assert "/tdw-api" in tdw

def test_no_crlf():
    for p in [ROOT/"index.html", ROOT/"projects.html", ROOT/"css/style.css", ROOT/"js/functions.js"]:
        data = p.read_bytes()
        assert b"\r\n" not in data, f"{p.name} still CRLF"

def test_backend_files_exist():
    for f in ["backend/get_spotify_info.py", "backend/requirements.txt", "backend/run-spotipy"]:
        assert (ROOT / f).exists()

def test_no_pi_files():
    assert not (ROOT / "Pi files").exists(), "Old Pi files dir should not exist"
    assert (ROOT / "backend").exists()

def test_html_doctype():
    for name in ["index.html", "projects.html", "certificates.html"]:
        text = (ROOT / name).read_text().lstrip()
        assert text.startswith("<!DOCTYPE html>"), f"{name} missing DOCTYPE"

def test_favicon_exists():
    assert (ROOT / "favicon.ico").exists()
