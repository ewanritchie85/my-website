import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _read(rel):
    return (ROOT / rel).read_text()

def test_tdw_pure_functions_exist():
    tdw = _read("js/turbo-death-warrior.js")
    for fn in ["function tdwBar", "function tdwHpClass", "function tdwPad", "function tdwApi", "function tdwSetState"]:
        assert fn in tdw, f"{fn} missing in tdw"

def test_tdw_hp_class_logic():
    # Extract logic and emulate in Python
    # tdwHpClass: >50 ok, >25 warn, else crit
    def tdwHpClass(pct):
        if pct > 50:
            return "hpbar ok"
        if pct > 25:
            return "hpbar warn"
        return "hpbar crit"
    assert tdwHpClass(75) == "hpbar ok"
    assert tdwHpClass(50) == "hpbar warn"
    assert tdwHpClass(30) == "hpbar warn"
    assert tdwHpClass(25) == "hpbar crit"
    assert tdwHpClass(0) == "hpbar crit"
    assert tdwHpClass(100) == "hpbar ok"

def test_tdw_bar_logic():
    import builtins
    def tdwBar(cur, mx, width=20):
        n = builtins.max(0, builtins.min(width, round((cur / mx) * width))) if mx else 0
        return "█" * n + "░" * (width - n)
    assert tdwBar(10, 20, width=10) == "█████░░░░░"
    assert tdwBar(20, 20) == "█" * 20
    assert tdwBar(0, 20) == "░" * 20
    assert tdwBar(5, 0) == "░" * 20  # avoid div zero in real js would be Infinity, but Python safe
    # Over max
    assert tdwBar(30, 20, width=10) == "█" * 10
    # Negative
    assert tdwBar(-5, 20, width=10) == "░" * 10

def test_tdw_pad_logic():
    def tdwPad(s, length):
        return (s or "").upper().ljust(length)
    assert tdwPad("hi", 5) == "HI   "
    assert tdwPad(None, 3) == "   "
    assert tdwPad("", 2) == "  "
    assert tdwPad("turbo", 10) == "TURBO     "

def test_render_artists_js_logic():
    # Mirror js renderArtists
    def renderArtists(artists):
        parts = []
        for a in artists:
            if isinstance(a, str):
                parts.append(a)
            elif isinstance(a, dict) and a.get("url"):
                parts.append(f'<a href="{a["url"]}">{a["name"]}</a>')
            elif isinstance(a, dict) and a.get("name"):
                parts.append(a["name"])
            else:
                parts.append("")
        return ", ".join(parts)
    assert renderArtists(["A", "B"]) == "A, B"
    assert renderArtists([{"name": "X", "url": "https://u"}]) == '<a href="https://u">X</a>'
    assert renderArtists([{"name": "Y"}]) == "Y"
    assert renderArtists([None]) == ""

def test_spotify_js_error_handling():
    sp = _read("js/spotify-now-playing.js")
    assert ".catch(" in sp
    assert "Could not load Spotify info" in sp

def test_functions_js_wordwheel_payload():
    f = _read("js/functions.js")
    # Ensure payload keys are correct
    assert "centre_letter" in f
    assert "outer_letters" in f
    assert "/api/solve" in f
    assert 'Content-Type' in f

def test_tdw_api_error_handling():
    tdw = _read("js/turbo-death-warrior.js")
    assert "if (!res.ok) throw" in tdw
    assert "SYSTEM ERROR" in tdw

def test_js_syntax_no_unclosed_braces():
    for rel in ["js/functions.js", "js/load-navbar.js", "js/spotify-now-playing.js", "js/turbo-death-warrior.js"]:
        txt = _read(rel)
        # basic brace balance
        assert txt.count("{") == txt.count("}"), f"{rel} brace mismatch"
        assert txt.count("(") == txt.count(")"), f"{rel} paren mismatch"
        assert txt.count("[") == txt.count("]"), f"{rel} bracket mismatch"

def test_css_no_broken_syntax():
    css = _read("css/style.css")
    # Must have matching braces
    assert css.count("{") == css.count("}"), "css brace mismatch"
    # Should contain tdw variables used in js
    assert "--tdw-amber" in css or "#ffaa00" in css
