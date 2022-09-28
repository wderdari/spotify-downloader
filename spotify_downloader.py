from __future__ import unicode_literals
import os
import spotipy
import yt_dlp
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import VideosSearch

# SECRET_KEY used for server-server authentication.
SECRET_KEY = os.environ.get("SECRET_KEY")


def error(msg):
    print(msg)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass


def get_top_tracks(track_lists):
    return track_lists


def my_hook(d):
    if d['status'] == 'finished':
        print("\nSuccessfully downloaded, proceeding with conversion.\n" + "Percentage Complete: " + d[
            '_percent_str'] + "\n")


def current_top_tracks():
    # Authentication allowing reading of playlists as defined by scope.
    scope = "user-top-read"

    # client ID & client secret to be filled by user.
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="e5556c4f8aa1455a9d2f4b5b84c70dfc",
                                                   client_secret=SECRET_KEY,
                                                   redirect_uri="http://127.0.0.1:8080", scope=scope))

    while True:
        limit = ""
        try:
            limit = int(input("-- Please specify the amount of top listened to tracks you would like to download "
                              "--\n"))
        except ValueError:
            print("Invalid input. Please specify a number.")
        break

    # API call to retrieve requested data. Formatted into list by sp
    data = sp.current_user_top_tracks(limit=limit)
    track_name = []
    # Retrieves the track name and artists and adds it to list.
    for item in data['items']:
        track_name.append(item['artists'][0]['name'] + " - " + item['name'])

    return track_name


def playlist_tracks():
    # Authentication allowing reading of playlists as defined by scope.
    scope = "playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="e5556c4f8aa1455a9d2f4b5b84c70dfc",
                                                   client_secret=SECRET_KEY,
                                                   redirect_uri="http://127.0.0.1:8080", scope=scope))

    # API call to retrieve requested data. Formatted into list by Spotipy.
    get_ids = sp.current_user_playlists(limit=5)
    playlist_ids = []
    for ids in get_ids['items']:
        playlist_ids.append(ids['id'])

    print("-- Please specify the playlist index you would like to download."
          "--\n")
    for i in range(len(playlist_ids)):
        print(f"[{i}] - " + get_ids['items'][i]['name'])

    index = int(input())
    # First parameter specifies playlist ID. A public playlist only, authentication required for private.
    tracks = sp.playlist_items(playlist_ids[index], limit=5)

    track_names = []

    for i in tracks['items']:
        track_names.append(i['track']['artists'][0]['name'] + " - " + i['track']['name'])

    return track_names


# Retrieves top result of YouTube search and adds it to a list containing URLs.
def find_url(tracks):
    track_url = []

    # Retrives URL for each track.
    for url in range(len(tracks)):
        video_search = VideosSearch(tracks[url], limit=len(tracks))
        track_url.append(video_search.result().get('result')[0]['id'])

    return track_url


if __name__ == '__main__':
    while True:
        scope_input = input("-- Please select your choice --\n"
                            "[0] - Download Top Listened Tracks\n[1] - Download Playlist\n")
        match scope_input:
            case "0":
                track_names = current_top_tracks()
                break
            case "1":
                track_names = playlist_tracks()
                break
            case _:
                print("Invalid choice\n")

    urls = find_url(track_names)

    ydl_opts = {
        'format': 'bestaudio/best',
        'forcefilename': True,
        'restrictfilenames': True,
        # Set desired path for storing temp and .mp3 files.
        "paths": {"temp": "/Users/wassimderdari/Documents/Python/spotify_downloader/Songs",
                  "home": "/Users/wassimderdari/Documents/Projects/Songs"},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('Downloading tracks...')
        for i in range(len(track_names)):
            # Force filename
            ydl_opts['outtmpl']['default'] = track_names[i] + '.'
            ydl.download(urls[i])
