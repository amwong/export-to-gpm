import pprint
import sys
import spotipy
import spotipy.util as util
from gmusicapi import Mobileclient

def get_username():
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Whoops, need your username!"
        print "usage: python Export to GPM.py [username]"
        sys.exit()
    return

def get_playlist_tracks(username, playlist_id):
    tracklist = []
    results = sp.user_playlist_tracks(username, playlist_id)   # returns dict of playlists track data
    tracks = results['items']                                  # list of tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items']) # adds all pages returned by spotipy to one list
    for i in range(len(tracks)):
        tracklist.append([tracks[i]['track']['name'], tracks[i]['track']['artists'][0]['name'],
        tracks[i]['track']['album']['name']]) # add track, artist, and album name to list
    return tracklist

def get_song_ids(tracklist):    # matches tracklist to GPM song IDs; reports tracks not found
    song_ids = []
    skipped_tracks = []
    skipped = 0
    for i in range(len(tracklist)):
        query = gpm.search(tracks[i][0].encode("utf8") + ' ' + tracks[i][1].encode("utf8"), max_results=1) # searches GPM for track + artist
        if len(query['song_hits']) > 0:                                      # if >0 results, add id to list
            songhitid = query['song_hits'][0]['track']['nid']
            song_ids.append(songhitid)
        else:
            skipped += 1
            skipped_tracks.append(tracks[i][0].encode("utf8") + ' ' + tracks[i][1].encode("utf8"))
    return song_ids, skipped_tracks

def write_list_to_file(list, file):
    for item in list:
        file.write('%s\n' % item)
    return

if __name__ == '__main__':

    # ********************
    # Gather tracks from Spotify:
    # ********************
    outputf = open('GPM Export Output Notes', 'w')
    username = 'YOUR SPOTIFY USERNAME'
    scope = 'playlist-read-private playlist-read-collaborative'
    playlist = 'YOUR PLAYLIST ID'
    token = util.prompt_for_user_token(username, scope, client_id='YOUR CLIENT ID',
            client_secret='YOUR CLIENT SECRET', redirect_uri='YOUR REDIRECT URI')

    if token:
        sp = spotipy.Spotify(auth=token) # start and authorize spotipy
        tracks = get_playlist_tracks(username, playlist) # get track, artist, and album names
    else:
        print "Can't get token for", username

    # ********************
    # Update GPM playlist:
    # ********************
    gpm = Mobileclient()
    gpm_username = 'YOUR GMAIL'
    gpm_password = 'YOUR PASSWORD'
    logged_in = gpm.login(gpm_username, gpm_password, Mobileclient.FROM_MAC_ADDRESS) # is true if log in successful

    if logged_in:
        gpm_song_ids, skipped_songs = get_song_ids(tracks)
        gpm_playlist_id = 'YOUR GPM PLAYLIST ID' #gpm.create_playlist('Export to GPM Test', description='Test playlist', public=False)
        for i in range(len(gpm_song_ids)):
            gpm.add_songs_to_playlist(gpm_playlist_id, gpm_song_ids[i])

        outputf.write('Number of tracks not found: %s' % skipped_songs)
        write_list_to_file(skipped_songs)
    else:
        print "Can't log in to GPM. Check credentials or connection."
