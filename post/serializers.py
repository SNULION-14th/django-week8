# post/serializers.py

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Artist, Song, SongArtist, Playlist, PlaylistSong, User

class SongSerializer(ModelSerializer):
    artists = serializers.SerializerMethodField()
    def get_artists(self, obj):
        song_artists = SongArtist.objects.filter(song=obj)
        return ArtistSerializer([sa.artist for sa in song_artists], many=True).data

    class Meta:
        model = Song
        fields = "__all__"

class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class PlaylistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    songs = serializers.SerializerMethodField()

    def get_songs(self, obj):
        playlist_songs = PlaylistSong.objects.filter(playlist=obj)
        return SongSerializer([ps.song for ps in playlist_songs], many=True).data

    class Meta:
        model = Playlist
        fields = "__all__"