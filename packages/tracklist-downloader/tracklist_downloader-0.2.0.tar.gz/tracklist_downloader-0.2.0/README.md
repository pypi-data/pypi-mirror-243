# Tracklist downloader

This project was created to download and manage my collection of songs from youtube and spotify.

It is intended to be run by providing a configuration that specifies youtube/spotify playlists to download in a specified path. 

It has multiple branches.
    * dev: contains the state (with tag v.0.0.1) of the POC that was ran once to download all my playlists from youtube.
    * dev-one_tracklist: dev branch for how to download one tracklist. can be merged and deleted
    * dev-list_of_tracklist: dev branch for downloading a list of tracklists. this was used in the POC.
    * dev-concurrent-list_of_tracklist: feature idea, use threadpools to submit jobs that concurrently download list of tracklists in parallel.


# Tracklist downloader flow

1. The CLI accepts a number of different options.
2. First it validates the provided configuration (spotify credentials, cookies file, configuration file, etc.)
3. Then it checks existing downloads (not yet implemented)
4. Then it downloads the playlists
5. And finally it runs some validation (removes false positive tracks that were mistakenly downloaded and provides a list of songs for each playlist that wasn't downloaded.)