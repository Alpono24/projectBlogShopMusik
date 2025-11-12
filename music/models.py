from django.db import models



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='music/artists/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    cover = models.ImageField(upload_to='music/albums/', blank=True, null=True)
    release_year = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.artist.name}"


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)
    audio_file = models.FileField(upload_to='music/songs/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} — {self.artist.name}"
