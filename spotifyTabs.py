
from pprint import pprint
from selenium import webdriver
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import spotipy
import spotipy.util as util
import time
import webbrowser


SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = '
# add your own spotify access token here
'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info


def main():
    current_track_id = None
    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)

        if current_track_info['id'] != current_track_id:
            current_track_id = current_track_info['id']
            current_track_name = current_track_info['track_name']
            current_track_artists = current_track_info['artists']
            printable = current_track_name + ' by ' + current_track_artists
            pprint("Finding tabs for " + printable + '...')

        # opens page for current song
            # search_string = ("https://www.songsterr.com/?pattern=")
            search_string = ("https://www.ultimate-guitar.com/search.php?search_type=title&value=")
            search_string = search_string.replace(' ', '%20')
            webbrowser.open(search_string + current_track_name)
            time.sleep(1)

if __name__ == '__main__':
    main()