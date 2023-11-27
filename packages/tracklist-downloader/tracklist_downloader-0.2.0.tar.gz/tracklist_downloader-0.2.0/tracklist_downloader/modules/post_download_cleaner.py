import json
import os
import logging
import shutil

from tracklist_downloader.helpers import remove_padding_zeros, get_spotify_playlist_songs
from tracklist_downloader.spotify_token_retriever import get_spotify_token
from tracklist_downloader.helpers import fetch_youtube_playlist_info


def validate_downloaded_songs(conf: dict, token: str, logger: logging.Logger) -> None:
    """
    Removes songs that were downloaded but don't appear in the playlist.

    This function checks each directory specified in the configuration file against the playlist data.
    Any song that was downloaded but not in the playlist is removed.

    Args:
    - conf (dict): Configuration data containing directory and playlist information.
    - logger (logging.Logger): Logger for recording activities.
    """
    for playlist in conf["spotify"]["playlists"]:
        folder_path = os.path.join(conf["target"], playlist["folder_name"])
        # Here, you would have a method to get the actual list of songs in the playlist
        # For now, assuming it's a list of song names
        playlist_songs = get_spotify_playlist_songs(playlist["url"], token)

        for song_name in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, song_name)):
                continue
            if song_name not in playlist_songs and not (song_name.endswith(".spotdl") or song_name.endswith(".txt") or song_name.endswith(".m3u")):
                song_path = os.path.join(folder_path, song_name)
                new_path = os.path.join(folder_path, "garbage", song_name)
                os.makedirs(os.path.join(folder_path, "garbage"), exist_ok=True)
                logger.info(f"Removing {song_name} from {folder_path}")
                shutil.move(song_path, new_path)
    for playlist in conf["youtube"]["playlists"]:
        folder_path = os.path.join(conf["target"], playlist["folder_name"])
        playlist_songs = fetch_youtube_playlist_info(playlist_url=playlist["url"])
        for song_name in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, song_name)):
                continue
            if song_name not in playlist_songs and not (song_name.endswith(".spotdl") or song_name.endswith(".txt") or song_name.endswith(".m3u")):
                song_path = os.path.join(folder_path, song_name)
                new_path = os.path.join(folder_path, "garbage", song_name)
                os.makedirs(os.path.dirname(os.path.join(folder_path, "garbage")), exist_ok=True)
                logger.info(f"Removing {song_name} from {folder_path}")
                shutil.move(song_path, new_path)



def validate_missing_songs(conf: dict, token: str, logger: logging.Logger) -> list:
    """
    Collects songs that were not downloaded but were listed on the playlist.

    This function checks each directory specified in the configuration file for missing songs
    by comparing the actual files in the directory against the playlist data.

    Args:
    - conf (dict): Configuration data containing directory and playlist information.
    - logger (logging.Logger): Logger for recording activities.

    Returns:
    - list: A list of dictionaries with each dictionary containing 'folder_name' and 'missing_songs'.
    """
    missing_songs_info = []

    spotify_missing_songs = []
    for playlist in conf["spotify"]["playlists"]:
        folder_path = os.path.join(conf["target"], playlist["folder_name"])
        playlist_songs = get_spotify_playlist_songs(playlist["url"], token)
        downloaded_songs = [song_name for song_name in os.listdir(folder_path)]

        missing_songs = [song for song in playlist_songs if song not in downloaded_songs]
        spotify_missing_songs.append({"folder_name": playlist["folder_name"], "missing_songs": missing_songs})


        for song in missing_songs:
            logger.warning(f"Missing song detected: {song} in {folder_path}")
    missing_songs_info.append({"spotify": spotify_missing_songs})

    youtube_missing_songs = []
    for playlist in conf["youtube"]["playlists"]:
        folder_path = os.path.join(conf["target"], playlist["folder_name"])
        playlist_songs = fetch_youtube_playlist_info(playlist["url"])
        downloaded_songs = [song_name for song_name in os.listdir(folder_path)]
        missing_songs = [song for song in playlist_songs if song not in downloaded_songs]
        youtube_missing_songs.append({"folder_name": playlist["folder_name"], "missing_songs": missing_songs})

        for song in missing_songs:
            logger.warning(f"Missing song detected: {song} in {folder_path}")
    missing_songs_info.append({"youtube": youtube_missing_songs})


    with open(os.path.join(conf["target"], "missing_songs.json"), "w") as file:
        json.dump(missing_songs_info, file, indent=4)

    return missing_songs_info


def download_songs(missing_songs: dict, logger: logging.Logger):
    """
    Downloads missing songs from YouTube and creates placeholder files if necessary.

    Args:
    - missing_songs (list): A list of dictionaries containing missing songs information.
    - logger (logging.Logger): Logger for recording download activities and failures.

    """
    # for directory in missing_songs:
    #     folder_path = directory['folder_name']
    #     for song in directory['missing_songs']:
    #         try:
    #             # Assuming you have a method to get the YouTube URL for the song
    #             youtube_url = get_youtube_url_for_song(song)
    #             download_command = ['yt-dlp', youtube_url, '-o', os.path.join(folder_path, f"{song}.%(ext)s")]
    #             subprocess.run(download_command, check=True)
    #             logger.info(f"Downloaded missing song: {song} in {folder_path}")
    #         except Exception as e:
    #             logger.error(f"Failed to download {song}: {e}")
    #             placeholder_path = os.path.join(folder_path, f"{song}.placeholder")
    #             open(placeholder_path, 'a').close()  # Create an empty placeholder file
    #             logger.info(f"Created placeholder for missing song: {song} in {folder_path}")


def post_download_cleanup(conf: dict, logger: logging.Logger):
    token = get_spotify_token(conf)
    remove_padding_zeros(conf)
    validate_downloaded_songs(conf, token, logger)
    missing_songs = validate_missing_songs(conf, token, logger)
    # TODO: automatically try to re-download songs
    # download_songs(missing_songs, logger)