from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from playlist_manager.models import Playlist, Track
from playlist_manager.spotify_client import SpotifyClient


class Command(BaseCommand):
    help = 'Build graph from wikipedia page links using Kevin Bacon as starting node'

    def add_arguments(self, parser):
        parser.add_argument("--playlist-id", type=str,
                            help="Playlist ID to dump to the database")

    def handle(self, **kwargs):
        playlist_id = kwargs["playlist_id"] if "playlist_id" in kwargs and kwargs["playlist_id"] else settings.DEFAULT_PLAYLIST_ID

        spotify_client = SpotifyClient()
        playlist_data = spotify_client.get_playlist(playlist_id)
        if not playlist_data:
            raise CommandError(f"Error fetching playlist {playlist_id}")
        else:
            formatted_track_data = spotify_client.format_playlist_data(playlist_data)
            playlist = Playlist.objects.create(
                **formatted_track_data["playlist"]
            )
            for track in formatted_track_data["tracks"]:
                track = Track.objects.create(**track)
                track.playlists.add(playlist)
            self.stdout.write(self.style.SUCCESS(f"Successfully dumped playlist {playlist_id} to the database"))
