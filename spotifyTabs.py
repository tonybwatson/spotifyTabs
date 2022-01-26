
from pprint import pprint
from selenium import webdriver
from spotipy.oauth2 import SpotifyClientCredentials
import databaseconfig
import PySimpleGUI as sg
import requests
import spotipy
import spotipy.util as util
import time
import webbrowser
# import databaseconfig1


SPOTIFY_GET_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
ACCESS_TOKEN = databaseconfig.ACCESS_TOKEN


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    json_resp = response.json()

    track_id = json_resp["item"]["id"]
    track_name = json_resp["item"]["name"]
    artists = [artist for artist in json_resp["item"]["artists"]]

    link = json_resp["item"]["external_urls"]["spotify"]

    artist_names = ", ".join([artist["name"] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info


def main():
    current_track_id = None

    # remastered = "(Remastered)"

    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)

        if current_track_info["id"] != current_track_id:
            current_track_id = current_track_info["id"]
            current_track_name = current_track_info["track_name"]
            current_track_artists = current_track_info["artists"]
            # if remastered in current_track_name:
            #         newcurrenttrackname = current_track_name.replace("(Remastered)", "")
            # USE THE ABOVE TO TAKE OUT THE WORD "REMASTERED" IN SEARCH TERMS - WILL PROBABLY HAVE TO DO BIG IF/ELSE. FINE FOR NOW - BUT PREVENTS SEARCH FROM FINDING ANYTHING. WILL PROBABLY FIND OTHER TERMS THAT ALSO PREVENT SEARCH.
            printable = current_track_name + " by " + current_track_artists
            pprint("Finding tabs for " + printable + "...")

        # opens page for current song
            # search_string = ("https://www.songsterr.com/?pattern=")
            search_string = ("https://www.ultimate-guitar.com/search.php?search_type=title&value=")
            search_string = search_string.replace(" ", "%20")
            if len(current_track_name) > 10: 
                webbrowser.open(search_string + current_track_name)
            else: 
                webbrowser.open(search_string + current_track_name + ' ' + current_track_artists)
            time.sleep(1)

if __name__ == "__main__":
    main()