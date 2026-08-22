import importlib
import sys
from unittest.mock import MagicMock, patch
import pytest

# Helper to reimport backend with mocked spotipy
def _import_backend(mock_spotify):
    # Remove cached backend module if present
    for mod in list(sys.modules.keys()):
        if mod.startswith("backend"):
            del sys.modules[mod]
    import backend.get_spotify_info as mod
    importlib.reload(mod)
    return mod

def test_artist_data_string_and_dict(mock_spotify):
    mod = _import_backend(mock_spotify)
    # string artist path via JS, but backend artist_data expects dicts
    # Test dict with external_urls and id fallback
    artists = [
        {"name": "A", "id": "1", "external_urls": {"spotify": "https://open.spotify.com/artist/1"}},
        {"name": "B", "id": "2", "external_urls": {}},
        {"name": "C", "external_urls": {}, "id": None},
    ]
    out = mod.artist_data(artists)
    assert out[0] == {"name": "A", "url": "https://open.spotify.com/artist/1"}
    assert out[1] == {"name": "B", "url": "https://open.spotify.com/artist/2"}
    assert out[2] == {"name": "C", "url": None}

def test_artist_data_empty(mock_spotify):
    mod = _import_backend(mock_spotify)
    assert mod.artist_data([]) == []

def test_spotify_info_empty_state(mock_spotify):
    mod = _import_backend(mock_spotify)
    # mock sp instance
    mod.sp.current_user_playing_track = MagicMock(return_value=None)
    mod.sp.current_user_top_tracks = MagicMock(return_value={"items": []})
    client = mod.app.test_client()
    resp = client.get("/spotify-info")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["currently_playing"] is None
    assert data["top_tracks"] == []

def test_spotify_info_currently_playing(mock_spotify):
    mod = _import_backend(mock_spotify)
    mock_track = {
        "name": "Test Track",
        "id": "t1",
        "artists": [{"name": "Artist1", "id": "a1", "external_urls": {"spotify": "https://open.spotify.com/artist/a1"}}],
        "album": {"images": [{"url": "https://img"}]},
        "external_urls": {"spotify": "https://open.spotify.com/track/t1"},
    }
    mod.sp.current_user_playing_track = MagicMock(return_value={"item": mock_track})
    mod.sp.current_user_top_tracks = MagicMock(return_value={"items": []})
    data = mod.app.test_client().get("/spotify-info").get_json()
    assert data["currently_playing"]["name"] == "Test Track"
    assert data["currently_playing"]["artists"][0]["name"] == "Artist1"
    assert data["currently_playing"]["album_art"] == "https://img"
    assert data["currently_playing"]["spotify_url"] == "https://open.spotify.com/track/t1"

def test_spotify_info_no_album_image(mock_spotify):
    mod = _import_backend(mock_spotify)
    mock_track = {
        "name": "NoImg",
        "artists": [],
        "album": {"images": []},
        "external_urls": {},
        "id": "x",
    }
    mod.sp.current_user_playing_track = MagicMock(return_value={"item": mock_track})
    mod.sp.current_user_top_tracks = MagicMock(return_value={"items": []})
    data = mod.app.test_client().get("/spotify-info").get_json()
    assert data["currently_playing"]["album_art"] is None
    # fallback url via id
    assert data["currently_playing"]["spotify_url"] == "https://open.spotify.com/track/x"

def test_spotify_info_top_tracks(mock_spotify):
    mod = _import_backend(mock_spotify)
    mod.sp.current_user_playing_track = MagicMock(return_value=None)
    top = {
        "items": [
            {"name": f"T{i}", "id": f"id{i}", "artists": [{"name": "A", "id": "a", "external_urls": {}}], "album": {"images": [{"url": f"https://img{i}"}]}, "external_urls": {}}
            for i in range(3)
        ]
    }
    mod.sp.current_user_top_tracks = MagicMock(return_value=top)
    data = mod.app.test_client().get("/spotify-info").get_json()
    assert len(data["top_tracks"]) == 3
    assert data["top_tracks"][0]["name"] == "T0"
    assert data["top_tracks"][0]["album_art"] == "https://img0"

def test_spotify_info_not_playing_null_item(mock_spotify):
    mod = _import_backend(mock_spotify)
    mod.sp.current_user_playing_track = MagicMock(return_value={"item": None})
    mod.sp.current_user_top_tracks = MagicMock(return_value={"items": []})
    data = mod.app.test_client().get("/spotify-info").get_json()
    assert data["currently_playing"] is None

def test_spotify_info_spotify_exception_401(mock_spotify):
    mod = _import_backend(mock_spotify)
    # Make the sp method raise SpotifyException
    mod.sp.current_user_playing_track = MagicMock(side_effect=mod.spotipy.SpotifyException("auth"))
    resp = mod.app.test_client().get("/spotify-info")
    assert resp.status_code == 401
    assert "error" in resp.get_json()

def test_spotify_info_generic_exception_500(mock_spotify):
    mod = _import_backend(mock_spotify)
    mod.sp.current_user_playing_track = MagicMock(side_effect=RuntimeError("boom"))
    resp = mod.app.test_client().get("/spotify-info")
    assert resp.status_code == 500
    assert "error" in resp.get_json()

def test_route_exists(mock_spotify):
    mod = _import_backend(mock_spotify)
    rules = [r.rule for r in mod.app.url_map.iter_rules()]
    assert "/spotify-info" in rules

def test_cache_path_env_override(monkeypatch, mock_spotify):
    monkeypatch.setenv("SPOTIPY_CACHE_PATH", "/tmp/custom.cache")
    # reimport to pick up env
    mod = _import_backend(mock_spotify)
    assert mod.CACHE_PATH == "/tmp/custom.cache"
