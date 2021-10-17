from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=200)
    popularity = models.PositiveSmallIntegerField()
    duration = models.PositiveIntegerField()
    artists = models.CharField(max_length=200)
    album_name = models.CharField(max_length=200)
    album_image = models.CharField(max_length=200)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.name

class TouristAttraction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)
    origin = models.BooleanField(default=False)
    destination = models.BooleanField(default=False)

    def __str__(self):
        return self.name
