# Spotify Export to GPM v0.1
Here's a first go at a music syncing Python script between Spotify and GPM. Only core functionality is currently working. The script takes all tracks in a Spotify playlist and matches them the best it can with songs on GPM. An output file named 'GPM Export Output Notes.txt' lists the number and tracknames of the titles not successfully matched.

## Requirements
[Spotipy](https://spotipy.readthedocs.io/en/latest/): Python library for the Spotify Web API

[gmusicapi](https://unofficial-google-music-api.readthedocs.io/en/latest/): an unofficial api for Google Play Music

## Quick start

1. Create an application at https://developer.spotify.com 
1. Get your client id and client secret key, setup a dummy redirect url (eg. 'http://localhost:8888/callback')
1. Setup your environment:
  ```
  export SPOTIPY_CLIENT_ID='your_client_id'
  export SPOTIPY_CLIENT_SECRET='your_client_secret'
  export SPOTIPY_REDIRECT_URI='your_redirect_url'
  ```
  
1. Enter required credentials into script (required entries are capitalized)

2. Run the script

  `$ python Export to GPM.py`
  
## Planned features
* Better credential entry
* Better querying/song matching
* Better playlist checking/updating
* Weekly scheduler for automatic playlist 'syncing'
