import json
import os
import subprocess
from urllib.parse import urlparse, parse_qs

import spotipy


def fetch_youtube_playlist_info(playlist_url):
    command = [
        "yt-dlp",
        "--dump-single-json",
        "--flat-playlist",
        playlist_url
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    playlist_info = json.loads(result.stdout)

    formatted_playlist_details = []
    for i, video in enumerate(playlist_info['entries'], start=1):
        formatted_title = f"{i} - {video['uploader']} - {video['title']}.flac"
        formatted_playlist_details.append(formatted_title)

    return formatted_playlist_details


def create_m3u_with_placeholders(playlist_url, download_directory, logger, m3u_filename='playlist.m3u'):
    playlist_info = fetch_youtube_playlist_info(playlist_url)
    downloaded_files = {file for file in os.listdir(download_directory) if file.endswith('.flac')}

    playlist_path = os.path.join(download_directory, m3u_filename)
    with open(playlist_path, 'w') as m3u_file:
        for index, title in enumerate(playlist_info):
            expected_filename = f"{index} - {title}.flac"
            if expected_filename in downloaded_files:
                m3u_file.write(os.path.join(download_directory, expected_filename) + '\n')
            else:
                m3u_file.write(f"# Missing: {title}\n")

    logger.info(f"M3U playlist created at: {playlist_path}")


def remove_padding_zeros(conf):
    target = conf["target"]
    for playlist in conf["youtube"]["playlists"]:
        target_directory = os.path.join(target, playlist["folder_name"])
        for filename in os.listdir(target_directory):
            if filename.startswith("0"):
                new_filename = filename.lstrip("0")
                os.rename(os.path.join(target_directory, filename), os.path.join(target_directory, new_filename))


def get_spotify_playlist_songs(url: str, token: str):
    # Parse the playlist ID from the URL
    parsed_url = urlparse(url)
    query_string = parse_qs(parsed_url.query)
    playlist_id = query_string.get('list')[0] if 'list' in query_string else parsed_url.path.split('/')[-1]

    # Authenticate with Spotify using the provided token
    sp = spotipy.Spotify(auth=token)

    # Fetch the playlist items
    results = sp.playlist_items(f"spotify:playlist:{playlist_id}")
    tracks = results['items']

    # Pagination
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Extract song information
    songs = []
    for i, item in enumerate(tracks):
        track = item['track']
        artist_names = track['artists'][0]['name']
        song_title = track['name']
        formatted_title = f"{i + 1} - {artist_names} - {song_title}.flac"
        songs.append(formatted_title)

    return songs
