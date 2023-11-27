import json
import logging
import os
import subprocess
import validators
import traceback

import spotipy

from pathlib import Path
from dotenv import load_dotenv

from tracklist_downloader.spotify_token_retriever import get_spotify_token

def check_ffmpeg_install(logger: logging.Logger) -> bool:
    """
    Checks if FFmpeg is installed and accessible in the system's PATH.

    This function attempts to run the FFmpeg command to check its version. It captures the output and
    return code of the command to determine if FFmpeg is installed and correctly set up in the system's PATH.
    It logs the result of this check using the provided logger.

    Args:
        logger (logging.Logger): Logger to record the status of the FFmpeg check.

    Returns:
        bool: True if FFmpeg is installed and accessible, False otherwise.

    Raises:
        FileNotFoundError: If the FFmpeg command is not found, indicating it's not installed or not in PATH.
    """
    try:
        # Attempt to run `ffmpeg -version` and capture its output
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            # If the return code is 0, FFmpeg is installed
            logger.info(f"FFmpeg is installed. Version info: {result.stdout}")
            return True
        else:
            # Non-zero return code indicates FFmpeg is not installed or not in PATH
            logger.error(f"FFmpeg is not installed or not found in PATH. {result.stderr}")
            return False
    except FileNotFoundError:
        # FileNotFoundError is raised if ffmpeg command is not found
        traceback_info = traceback.format_exc()
        logger.error(f"FFmpeg is not installed or not found in PATH. {traceback_info}")
        return False


def log_error(msg: str, logger: logging.Logger, validation_type: str) -> None:
    """
    Logs an error message. Raises an exception if the validation type is 'hard'.

    Args:
    - msg (str): The error message to log.
    - logger (logging.Logger): Logger to use for logging the error.
    - validation_type (str): Type of validation ('hard', 'soft', 'none'). Raises exception if 'hard'.

    Returns:
    - None
    """
    logger.error(msg)
    if validation_type == "hard":
        raise


def validate_cookies_file(config: dict, logger: logging.Logger) -> bool:
    """
    Validates the existence and file type of a cookies file specified in the configuration.

    This function checks whether the cookies file path is provided in the configuration and verifies its
    existence and file type. It logs the outcome of these validations using the provided logger.

    Args:
        config (dict): Configuration dictionary containing the 'cookies_path' key.
        logger (logging.Logger): Logger for recording the validation process and any errors encountered.

    Returns:
        bool: True if the cookies file exists and is a file, False otherwise.
    """
    cookies_path = config.get("cookies_path")
    if not cookies_path:
        logger.warning("No cookie file provided.")
        return False
    cookies_path = Path(cookies_path)
    if not cookies_path.exists():
        logger.error(f"FileNotFoundError: The specified path '{cookies_path}' does not exist.")
        return False
    if not os.path.isfile(cookies_path):
        logger.error("Cookie path is not a file.")
        return False
    return True


def validate_env(conf) -> bool:
    """
    Validates the existence of a .env file in the current directory.

    Returns:
    - bool: True if .env file exists, False otherwise.
    """
    if not os.path.isfile(conf[".env_path"]):
        return False
    return True


def validate_spotify_credentials(conf) -> bool:
    """
    Validates the presence of Spotify credentials (client ID and secret) in the environment.

    Returns:
    - bool: True if both client ID and secret are available, False otherwise.
    """
    load_dotenv(conf[".env_path"])
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or not client_secret:
        return False
    return True


def validate_target(target: str) -> None:
    """
    Validates the provided target path.

    Args:
    - target (str): The target path to validate.

    Raises:
    - ValueError: If the input path string is empty.
    - FileNotFoundError: If the specified path does not exist.
    - NotADirectoryError: If the specified path is not a directory.

    Returns:
    - None
    """
    if not target:
        raise ValueError("The input path string is empty. Please provide a valid path.")
    target_path = Path(target)
    if not target_path.exists():
        raise FileNotFoundError(f"The specified path '{target_path}' does not exist.")
    if not target_path.is_dir():
        raise NotADirectoryError(f"The specified path '{target_path}' is not a directory.")


def validate_dict_structure(data_dict: dict, main_key: str) -> bool:
    """
    Validates the structure of a dictionary based on a specified key and sub-keys.

    Args:
    - data_dict (dict): The dictionary to validate.
    - main_key (str): The main key to look for in the dictionary.

    Returns:
    - bool: True if the structure is as expected, False otherwise.
    """
    # Check if the main key exists in the dictionary
    if main_key not in data_dict:
        return False
        # raise KeyError(f"The key '{main_key}' is missing from the dictionary.")

    # Check if 'playlists' and 'cache' keys exist within the main key
    for sub_key in ['playlists', 'cache']:
        if sub_key not in data_dict[main_key]:
            return False
            # raise KeyError(f"The key '{sub_key}' is missing under '{main_key}'.")

        # Check if the value for each sub_key is a list
        if not isinstance(data_dict[main_key][sub_key], list):
            return False
            # raise ValueError(f"The value for '{sub_key}' under '{main_key}' is not a list.")
    return True


def validate_spotify_config(conf: dict) -> bool:
    """
    Validates the Spotify configuration section of the provided configuration dictionary.

    Args:
    - conf (dict): Configuration dictionary containing the Spotify configuration.

    Returns:
    - bool: True if the Spotify configuration is valid, False otherwise.
    """
    return validate_dict_structure(conf, "spotify")


def validate_youtube_config(conf: dict) -> bool:
    """
    Validates the YouTube configuration section of the provided configuration dictionary.

    Args:
    - conf (dict): Configuration dictionary containing the YouTube configuration.

    Returns:
    - bool: True if the YouTube configuration is valid, False otherwise.
    """
    return validate_dict_structure(conf, "youtube")


def validate_folder_name(playlist_conf: dict) -> bool:
    """
    Validates the presence of a 'folder_name' key in the provided playlist configuration.

    Args:
    - playlist_conf (dict): Playlist configuration dictionary to validate.

    Returns:
    - bool: True if 'folder_name' key exists, False otherwise.
    """
    if "folder_name" not in playlist_conf.keys():
        return False
    return True


def validate_url(playlist_conf: dict, provider: str, access_token: str = None) -> bool:
    """
    Validates the URL in the playlist configuration for the given provider.

    Args:
    - playlist_conf (dict): Playlist configuration containing the URL to validate.
    - provider (str): The provider name (e.g., 'Spotify', 'YouTube').
    - access_token (str, optional): Access token for API calls if needed. Default is None.

    Returns:
    - bool: True if the URL is valid, False otherwise.
    """
    if "url" not in playlist_conf.keys():
        raise KeyError(f"The key 'url' is missing.")

    if not validators.url(playlist_conf["url"]):
        raise ValueError(f"Invalid url for {playlist_conf['folder_name']}.")

    if provider == "spotify":
        sp = spotipy.Spotify(auth=access_token)
        playlist_details = sp.playlist(playlist_conf["url"])

        # Check if the playlist is public
        if not playlist_details['public']:
            return False
            # raise ValueError("Playlist is not public.")

    elif provider == "youtube":
        # Run youtube-dlp command to fetch playlist info
        result = subprocess.run(['yt-dlp', '--dump-json', '--flat-playlist', playlist_conf["url"]],
                                capture_output=True, text=True)

        # Check if there was an error
        if result.returncode != 0:
            return False

        return True
    else:
        raise ValueError(f"unexpected provider. Expected spotify or youtube, got: {provider}")
    return True


def validate_config(path: Path, validation_type: str, logger: logging.Logger) -> dict:
    """
    Validates the configuration for the spotLy application, considering various application requirements.

    This function checks the validity of the provided configuration file, including the existence and
    correctness of target paths, playlist URLs, folder names, and .env file with Spotify credentials.
    The type of validation ('hard', 'soft', or 'none') dictates the function's behavior in case of
    validation failures. The process and results of validation are logged using the provided logger.

    Args:
        path (Path): The path to the configuration file.
        validation_type (str): The level of validation - 'hard', 'soft', or 'none'.
        logger (logging.Logger): Logger instance for recording the process and errors.

    Returns:
        dict: The parsed and validated configuration data from the file.

    Raises:
        Exception: In case of 'hard' validation, if any validation fails.

    Notes:
        - 'Hard' validation throws exceptions on failures and halts execution.
        - 'Soft' validation logs errors and continues execution despite failures.
        - 'None' validation bypasses all checks and returns the configuration directly.
    """
    abs_path = path.resolve()
    with open(abs_path) as file:
        config = json.load(file)
    if validation_type == "none":
        return config

    try:
        validate_target(config["target"])
        logger.info("Target path valid.")
    except (ValueError, FileNotFoundError, NotADirectoryError) as e:
        traceback_info = traceback.format_exc()
        logger.error(traceback_info)
        raise

    if validate_cookies_file(config, logger):
        logger.info("Cookies.txt found and valid")

    if not validate_spotify_config(config):
        log_error("Invalid spotify config.", logger, validation_type)
    if not validate_env(config):
        log_error("FileNotFoundError: .env file not found.", logger, validation_type)
    if not validate_spotify_credentials(config):
        log_error("Error: Invalid or missing Spotify credentials in .env file.", logger, validation_type)
    if validate_spotify_config(config) and validate_env(config) and validate_spotify_credentials(config):
        logger.info("Spotify configuration and spotify credentials validated")
    # want to continue execution regardless if previous conditions are validated.
    # (in case of hard - exceptions stops, in case of soft we still want to execute)
    access_token = get_spotify_token(config)
    for spotify_playlist in config["spotify"]["playlists"]:
        if not validate_folder_name(spotify_playlist):
            log_error("The key 'folder_name' is missing.", logger, validation_type)
        if not validate_url(spotify_playlist, "spotify", access_token=access_token):
            log_error(f"Error: {spotify_playlist['url']} does not exist or cannot be accessed.", logger,
                      validation_type)
            continue
        logger.info(f"{spotify_playlist['url']} is public")

    if not validate_youtube_config(config):
        log_error("invalid youtube config", logger, validation_type)

    if validate_youtube_config(config) and not check_ffmpeg_install(logger):
        raise Exception("Found youtube playlists, but no ffmpeg is installed. Please install it from: "
                        "https://ffmpeg.org/download.html")
    for youtube_playlist in config["youtube"]["playlists"]:
        if not validate_folder_name(youtube_playlist):
            log_error("The key 'folder_name' is missing.", logger, validation_type)
        if not validate_url(youtube_playlist, "youtube"):
            log_error(f"Error: {youtube_playlist['url']} does not exist or cannot be accessed.", logger,
                      validation_type)
            continue
        logger.info(f"{youtube_playlist['url']} is public")
    return config
