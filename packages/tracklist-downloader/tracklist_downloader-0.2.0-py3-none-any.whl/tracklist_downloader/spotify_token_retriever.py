import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import os
import time
import json

from dotenv import load_dotenv

cache_filename = 'spotify_token_cache.json'
PORT = 5001

def set_spotify_credentials_from_env(config):
    # Load environment variables from .env file
    load_dotenv(config[".env_path"])

    # Set environment variables
    os.environ['SPOTIFY_CLIENT_ID'] = os.getenv('SPOTIFY_CLIENT_ID')
    os.environ['SPOTIFY_CLIENT_SECRET'] = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Optional: Print a message to confirm that the environment variables are set
    print("Spotify credentials set from .env file.")

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/callback'):
            self.send_response(200)
            self.end_headers()
            self.server.path = self.path  # Store the path in the server instance
            self.wfile.write(b'You can now close this tab.')
            self.server.path = self.path  # Store the path in the server instance
            threading.Thread(target=self.server.shutdown).start()  # Shutdown the server

def start_server(server_class=HTTPServer, handler_class=RequestHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    threading.Thread(target=httpd.serve_forever).start()
    return httpd  # Return the server instance
def stop_server(httpd):
    httpd.shutdown()  # Shutdown the server
def get_spotify_token(config, timeout=30):
    current_time = time.time()
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r') as file:
            cache = json.load(file)
            if cache['token'] and cache['expires_at'] > current_time:
                return cache['token']

    set_spotify_credentials_from_env(config)
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=f'http://127.0.0.1:{PORT}/callback',
        scope='playlist-read-private'
    )

    httpd = start_server()
    webbrowser.open(auth_manager.get_authorize_url())

    start_time = time.time()
    while not hasattr(httpd, 'path') and time.time() - start_time < timeout:
        time.sleep(0.1)  # Prevent busy waiting

    if not hasattr(httpd, 'path'):
        stop_server(httpd)
        raise TimeoutError("Authentication timed out. Please check your credentials and internet connection.")

    code = auth_manager.parse_response_code(httpd.path)
    token_info = auth_manager.get_access_token(code)

    with open(cache_filename, 'w') as file:
        cache = {
            'token': token_info["access_token"],
            'expires_at': token_info["expires_at"]
        }
        json.dump(cache, file)
    return token_info["access_token"]

if __name__ == "__main__":
    try:
        token = get_spotify_token(config)
        print(token)
    except TimeoutError:
        print("Invalid spotify credentials. couldn't validate playlists.")
    except spotipy.SpotifyOauthError as oauth_err:
        print(f"OAuth error: {oauth_err}")
    except Exception as general_err:
        print(f"An error occurred: {general_err}")
