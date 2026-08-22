import os
import sys
from pathlib import Path
import pytest

# Ensure repo root is on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Default env for imports that require Spotify creds
os.environ.setdefault("SPOTIPY_CLIENT_ID", "test_id")
os.environ.setdefault("SPOTIPY_CLIENT_SECRET", "test_secret")
os.environ.setdefault("SPOTIPY_REDIRECT_URI", "http://localhost/callback")

@pytest.fixture
def mock_spotify(monkeypatch):
    """Provide a mocked spotipy module before importing backend."""
    import types
    mock_mod = types.ModuleType("spotipy")
    mock_oauth = types.ModuleType("spotipy.oauth2")

    class FakeSpotifyOAuth:
        def __init__(self, *a, **kw):
            pass

    class FakeSpotify:
        def __init__(self, *a, **kw):
            pass
        def current_user_playing_track(self):
            return None
        def current_user_top_tracks(self, limit=10, time_range='short_term'):
            return {"items": []}

    mock_mod.Spotify = FakeSpotify
    mock_oauth.SpotifyOAuth = FakeSpotifyOAuth
    # need SpotifyException for except branch
    class SpotifyException(Exception):
        pass
    mock_mod.SpotifyException = SpotifyException

    monkeypatch.setitem(sys.modules, "spotipy", mock_mod)
    monkeypatch.setitem(sys.modules, "spotipy.oauth2", mock_oauth)
    return mock_mod
