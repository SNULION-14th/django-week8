from django.db import models

class Artist(models.Model):
    artist_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta: #메타 데이터
        db_table = '가수'
    
    def __str__(self):
        return self.name


class Song(models.Model):
    song_key = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    lowest_pitch = models.CharField(max_length=10)
    highest_pitch = models.CharField(max_length=10)

    class Meta:
        db_table = '노래'

    def __str__(self):
        return self.title


class SongArtist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE) #부모 삭제될때 함꼐 삭제
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

    class Meta:
        db_table = '노래+가수'
        unique_together = ('song', 'artist')

    def __str__(self):
        return f"{self.song.title} - {self.artist.name}"


class User(models.Model):
    user_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    lowest_pitch = models.CharField(max_length=10)
    highest_pitch = models.CharField(max_length=10)

    class Meta:
        db_table = '회원'
    
    def __str__(self):
        return self.name


class Playlist(models.Model):
    playlist_key = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = '플레이리스트'

    def __str__(self):
        return f"{self.user.name}'s {self.name}"


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        db_table = '플레이리스트+노래'
        unique_together = ('playlist', 'song')

    def __str__(self):
        return f"{self.playlist.name} - {self.song.title}"