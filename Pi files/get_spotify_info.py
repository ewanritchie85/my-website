import os
import logging
from dotenv import load_dotenv
from flask import Flask, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configure logging for headless environments
logging.basicConfig(level=logging.INFO)

# Set cache path securely in the same directory as the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(BASE_DIR, ".cache-spotify")

# Initialize Spotify Auth ONCE at startup
auth_manager = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-read-currently-playing user-top-read',
    cache_path=CACHE_PATH,
    open_browser=False
)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route('/spotify-info')
def spotify_info():
    try:
        # 1. Fetch currently playing track
        current = sp.current_user_playing_track()
        current_track = None
        
        if current and current.get('item'):
            track = current['item']
            current_track = {
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'spotify_url': track.get('external_urls', {}).get('spotify') or (
                    f"https://open.spotify.com/track/{track['id']}" if track.get('id') else None
                )
            }

        # 2. Fetch Top 10 tracks
        top_tracks_data = sp.current_user_top_tracks(limit=10, time_range='short_term')
        top_tracks = []
        
        if top_tracks_data and 'items' in top_tracks_data:
            for item in top_tracks_data['items']:
                top_tracks.append({
                    'name': item['name'],
                    'artists': [artist['name'] for artist in item['artists']],
                    'album_art': item['album']['images'][0]['url'] if item['album']['images'] else None,
                    'spotify_url': item.get('external_urls', {}).get('spotify') or (
                        f"https://open.spotify.com/track/{item['id']}" if item.get('id') else None
                    )
                })

        return jsonify({
            'currently_playing': current_track,
            'top_tracks': top_tracks
        })

    except spotipy.SpotifyException as e:
        logging.error(f"Spotify API error: {e}")
        return jsonify({'error': 'Spotify API authentication or fetch failed. Check terminal.'}), 401
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Failed to fetch Spotify data'}), 500

if __name__ == '__main__':
    # Run on all network interfaces on port 5050
    app.run(host='0.0.0.0', port=5050)