import http.server
import threading
import socket
import time
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]

def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def test_static_server_smoke():
    port = _free_port()
    handler = http.server.SimpleHTTPRequestHandler
    import os
    orig = os.getcwd()
    os.chdir(ROOT)
    httpd = http.server.HTTPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)
    try:
        for path, expect in [
            ("/", 200),
            ("/index.html", 200),
            ("/projects.html", 200),
            ("/certificates.html", 200),
            ("/css/style.css", 200),
            ("/js/functions.js", 200),
            ("/js/load-navbar.js", 200),
            ("/js/spotify-now-playing.js", 200),
            ("/js/turbo-death-warrior.js", 200),
            ("/navbar.html", 200),
            ("/favicon.ico", 200),
            ("/nonexistent.html", 404),
            ("/style.css", 404),
            ("/functions.js", 404),
        ]:
            url = f"http://127.0.0.1:{port}{path}"
            try:
                with urllib.request.urlopen(url) as r:
                    code = r.status
            except urllib.error.HTTPError as e:
                code = e.code
            assert code == expect, f"{path} expected {expect} got {code}"
    finally:
        httpd.shutdown()
        os.chdir(orig)

def test_html_refs_resolve():
    from bs4 import BeautifulSoup
    for name in ["index.html", "projects.html", "certificates.html"]:
        soup = BeautifulSoup((ROOT / name).read_text(), "html.parser")
        for tag in soup.find_all(["link", "script", "img"]):
            src = tag.get("href") or tag.get("src")
            if not src:
                continue
            if src.startswith("http") or src.startswith("//"):
                continue
            clean = src.split("?")[0].lstrip("./")
            if not clean:
                continue
            assert (ROOT / clean).exists(), f"{name} refs missing {src} -> {clean}"
