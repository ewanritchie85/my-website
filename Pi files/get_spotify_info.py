#This script is just for reference and is being run on my raspberry pi to get the currently playing track from Spotify. 
# It uses the spotipy library, which is a Python client for the Spotify Web API. Make sure to replace the placeholders with 
# your actual Spotify API credentials and set up the redirect URI properly.


import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)

def get_spotify_client():
    CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
    REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
    scope = 'user-read-currently-playing user-top-read'
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        open_browser=False
    ))

@app.route('/spotify-info')
def spotify_info():
    sp = get_spotify_client()
    # Currently playing track
    current = sp.current_user_playing_track()
    if current and current.get('item'):
        track = current['item']
        current_track = {
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'spotify_url': track.get('external_urls', {}).get('spotify') if track.get('external_urls') else (f"https://open.spotify.com/track/{track.get('id')}" if track.get('id') else None)
        }
    else:
        current_track = None

    # Top 10 tracks for the last ~30 days
    top_tracks_data = sp.current_user_top_tracks(limit=10, time_range='short_term')
    top_tracks = []
    for item in top_tracks_data['items']:
        top_tracks.append({
            'name': item['name'],
            'artists': [artist['name'] for artist in item['artists']],
            'album_art': item['album']['images'][0]['url'] if item['album']['images'] else None,
            'spotify_url': item.get('external_urls', {}).get('spotify') if item.get('external_urls') else (f"https://open.spotify.com/track/{item.get('id')}" if item.get('id') else None)
        })

    return jsonify({
        'currently_playing': current_track,
        'top_tracks': top_tracks
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)