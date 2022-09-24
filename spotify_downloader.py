from __future__ import unicode_literals
import spotipy
import yt_dlp
from spotipy.oauth2 import SpotifyOAuth
from youtubesearchpython import VideosSearch


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def get_top_tracks(track_lists):
    return track_lists


def my_hook(d):
    if d['status'] == 'finished':
        print("\nSuccessfully downloaded, proceeding with conversion.\n" + "Percentage Complete: " + d[
            '_percent_str'] + "\n")


def current_top_tracks():
    # Authentication allowing reading of playlists as defined by scope.
    scope = "playlist-read-collaborative"

    # Client ID
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                                   client_secret="",
                                                   redirect_uri="http://127.0.0.1:8080", scope=scope))

    # API call to retrieve requested data. Formatted into list by sp
    data = sp.current_user_top_tracks(limit=10)

    track_names = []
    # Retrieves the track name and artists and adds it to list.
    for item in data['items']:
        track_names.append(item['artists'][0]['name'] + " - " + item['name'])

    return track_names


def playlist_tracks():
    # Authentication allowing reading of playlists as defined by scope.
    scope = "playlist-read-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="e5556c4f8aa1455a9d2f4b5b84c70dfc",
                                                   client_secret="87b423f05fd24d44a3be426fd42df827",
                                                   redirect_uri="http://127.0.0.1:8080", scope=scope))

    # API call to retrieve requested data. Formatted into list by Spotipy.
    get_ids = sp.current_user_playlists(limit=10)
    playlist_ids = []
    for identifier in get_ids['items']:
        playlist_ids.append(identifier['id'])

    print(playlist_ids)

    # First parameter specifies playlist ID. A public playlist only, authentication required for private.
    tracks = sp.playlist_items("4IrbtF43ZGjnJOxquLaJE0", limit=10)

    track_names = []

    for i in tracks['items']:
        track_names.append(i['track']['artists'][0]['name'] + " - " + i['track']['name'])

    return track_names


# Retrieves top result of YouTube search and adds it to a list containing URLs.
def find_url(list_names):
    track_list = []

    for i in range(len(list_names)):
        video_search = VideosSearch(list_names[i], limit=1)
        track_list.append(video_search.result())
        i += 1

    track_urls = []

    for results in track_list:
        track_urls.append(results['result'][0]['link'])

    return track_urls


if __name__ == '__main__':
    track_names = playlist_tracks()
    urls = find_url(track_names)

    ydl_opts = {
        'format': 'bestaudio/best',
        'forcefilename': True,
        'restrictfilenames': True,
        'outtmpl': "%(title)s.",
        # Set desired path for storing temp and .mp3 files.
        # "paths": {"temp": "/Users/wassimderdari/Documents/Python/spotify_downloader/Songs",
        #           "home": "/Users/wassimderdari/Documents/Python/spotify_downloader/Songs"},
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
        ydl.download(urls)