"""
Should the validator pop playlists that aren't validated?
Should this depend on the validation type?


"""
import logging
import os
import subprocess

from tracklist_downloader.modules.logging_module import FileErrorHandler
from tracklist_downloader.helpers import create_m3u_with_placeholders
from tracklist_downloader.spotify_token_retriever import get_spotify_token


def download_playlist(command: list, logger: logging.Logger) -> None:
    """
    Executes a download command for a playlist and logs the output.

    This function runs a subprocess command to download a playlist (Spotify or YouTube). It captures
    the standard output and error streams. In case of errors, these are logged as error messages.
    Successful outputs are logged as informational messages.

    Args:
    - command (list): A list of command-line arguments to be executed.
    - logger (logging.Logger): Logger instance for recording the subprocess outputs.

    Returns:
    - None
    """
    # Run the subprocess command with output and error capture
    result = subprocess.run(command, check=False, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # Check if the subprocess call was successful
    if result.returncode != 0:
        # Log an error message if there was an error
        logger.error(f"Error occurred: {result.stderr}")
    else:
        # Log an info message if the command was successful
        logger.info(result.stdout)


def download_spotify_playlist(playlist: dict, target, token, logger: logging.Logger, cookies_path: str = None) -> None:
    """
    Downloads a Spotify playlist using the spotdl command.

    Constructs and executes a spotdl command to download tracks from a specified Spotify playlist.
    The download progress and errors, if any, are logged using the provided logger.

    Args:
    - playlist (dict): A dictionary containing the Spotify playlist details, including the URL.
    - logger (logging.Logger): Logger instance for recording the download process and errors.

    Returns:
    - None
    """
    command = [
        "spotdl",
        "--audio", "youtube-music",
        "--only-verified-results",
        "--auth-token", token,
        "--cache-path", f"{target}/{playlist['folder_name']}",
        "--threads", "6",
        "--bitrate", "320k",
        "--format", "flac",
        "--save-file", f"{target}/{playlist['folder_name']}/path_to_downloaded.spotdl",
        "--output", f"{target}/{playlist['folder_name']}/" + "{list-position} - {artists} - {title}.{output-ext}",
        "--overwrite", "force",
        "--scan-for-songs",
        "--save-errors", f"{target}/{playlist['folder_name']}/errors.txt",
        "--playlist-numbering",
        "--ytm-data",
        # "--yt-dlp-args", "YT_DLP_ARGUMENTS",
        "--add-unavailable",
        "--m3u", f"{target}/{playlist['folder_name']}/{playlist['folder_name']}.m3u"
    ]
    if not cookies_path:
        command.append(["--cookie-file", cookies_path])
    command.append(playlist["url"])
    download_playlist(command, logger)


def download_youtube_playlist(playlist: dict, target, logger: logging.Logger, cookies_path: str = None) -> None:
    """
    Downloads a YouTube playlist using yt-dlp.

    Constructs and executes a yt-dlp command to download videos from a specified YouTube playlist.
    The download progress and errors, if any, are logged using the provided logger.

    Args:
    - playlist (dict): A dictionary containing the YouTube playlist details, including the URL.
    - logger (logging.Logger): Logger instance for recording the download process and errors.

    Returns:
    - None
    """
    # Create a file error handler and add it to the logger
    error_log_path = os.path.join(target, playlist["folder_name"], 'errors.txt')
    file_error_handler = FileErrorHandler(error_log_path)
    file_error_handler.setLevel(logging.ERROR)
    logger.addHandler(file_error_handler)

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "flac",
        "--audio-quality", "0",
        "--output", f"{target}/{playlist['folder_name']}/%(playlist_index)s - %(uploader)s - %(title)s.%(ext)s",
        "--ignore-errors",
        "--no-overwrites",
        "--yes-playlist",
        "--download-archive", f"{target}/{playlist['folder_name']}/path_to_downloaded.txt"
    ]
    if not cookies_path:
        command.append(["--cookies", cookies_path])
    command.append(playlist['url'])
    download_playlist(command, logger)

    # Remove the file error handler after download is complete
    logger.removeHandler(file_error_handler)

    create_m3u_with_placeholders(playlist_url=playlist["url"],
                                 download_directory=f"{target}/{playlist['folder_name']}",
                                 logger=logger,
                                 m3u_filename=f"{playlist['folder_name']}.m3u")



def download(config: dict, logger: logging.Logger) -> None:
    """
    Initiates the download process for both Spotify and YouTube playlists as per configuration.

    Iterates through each playlist in the provided configuration, initiating the download process for both
    Spotify and YouTube playlists. The function relies on separate handlers for each platform. It logs the
    progress and any errors encountered during the download process.

    Args:
    - config (dict): Configuration data containing playlists for Spotify and YouTube.
    - logger (logging.Logger): Logger instance to record the overall download process.

    Returns:
    - None
    """
    target = config["target"]
    token = get_spotify_token(config)
    cookies_path = config.get("cookies_path")
    for playlist in config["spotify"]["playlists"]:
        download_spotify_playlist(playlist, target, token, logger, cookies_path)
    for playlist in config["youtube"]["playlists"]:
        download_youtube_playlist(playlist, target, logger, cookies_path)
