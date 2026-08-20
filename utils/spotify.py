import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

def get_spotify_client():
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return None
        
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    ))

def is_spotify_url(url):
    return "spotify.com" in url

def get_track_name(url):
    sp = get_spotify_client()
    if not sp:
        return None

    try:
        if "track" in url:
            track = sp.track(url)
            return f"{track['name']} {track['artists'][0]['name']}"
        elif "album" in url:
            # We'll just take the first track for simplicity in this basic setup
            album = sp.album_tracks(url)
            track = album['items'][0]
            return f"{track['name']} {track['artists'][0]['name']}"
        elif "playlist" in url:
            # Take the first track of the playlist
            playlist = sp.playlist_tracks(url)
            track = playlist['items'][0]['track']
            return f"{track['name']} {track['artists'][0]['name']}"
    except Exception as e:
        print(f"Spotify extraction error: {e}")
        return None
    return None
