import logging

from django.conf import settings

import requests


logger = logging.getLogger(__name__)


class SpotifyClient(object):
    def __init__(self) -> None:
        self.HOST = "https://api.spotify.com/v1"
        self.ACCESS_TOKEN = settings.SPOTIFY_ACCESS_TOKEN
        self.HEADERS = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}"
        }
        self.PLAYLIST_IMAGE_LIST_INDEX = 0
        self.TRACK_IMAGE_DIMENSION_300 = 1

    def get_playlist(self, playlist_id: str = None) -> dict:
        """Returns a playlist data"""
        playlist_id = playlist_id if playlist_id else settings.DEFAULT_PLAYLIST_ID

        url = f"{self.HOST}/playlists/{playlist_id}"
        response = requests.get(url, headers=self.HEADERS)
        response_json = response.json()
        if "error" in response_json:
            print(response_json)
            logger.error(
                f"Error fetching playlist {playlist_id}",
                extra={"response_json": response_json, "status_code": response.status_code}
            )
            return {}
        else:
            return response_json

    def format_playlist_data(self, playlist_data: dict) -> list:
        """Format playlist with data that will be displayed"""
        playlist_tracks = playlist_data["tracks"]["items"]
        
        formatted_playlist_tracks = {
            "playlist": {
                "name": playlist_data["name"],
                "description": playlist_data["description"],
                "image": playlist_data["images"][self.PLAYLIST_IMAGE_LIST_INDEX]["url"]
            },
            "tracks": []
        }

        for track in playlist_tracks:
            artists = [artist["name"] for artist in track["track"]["artists"]]
            artists_names = ', '.join([artist for artist in artists])

            playlist_track_data = {
                "album_name": track["track"]["album"]["name"],
                "album_image": track["track"]["album"]["images"][self.TRACK_IMAGE_DIMENSION_300]["url"],
                "artists": artists_names,
                "name": track["track"]["name"],
                "popularity": track["track"]["popularity"],
                "duration": track["track"]["duration_ms"],
            }
            formatted_playlist_tracks["tracks"].append(playlist_track_data)
        return formatted_playlist_tracks
