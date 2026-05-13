from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Artist, Song, SongArtist, Playlist, PlaylistSong, User


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    artists = serializers.SerializerMethodField()

    @extend_schema_field(ArtistSerializer(many=True))
    def get_artists(self, obj):
        return ArtistSerializer(
            [song_artist.artist for song_artist in obj.songartist_set.all()],
            many=True,
        ).data

    class Meta:
        model = Song
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.all(),
        write_only=True,
    )
    songs = serializers.SerializerMethodField()

    @extend_schema_field(SongSerializer(many=True))
    def get_songs(self, obj):
        return SongSerializer(
            [playlist_song.song for playlist_song in obj.playlistsong_set.all()],
            many=True,
        ).data

    class Meta:
        model = Playlist
        fields = ("playlist_key", "user", "user_id", "name", "songs")


class SongArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongArtist
        fields = "__all__"


class PlaylistSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistSong
        fields = "__all__"


class SongArtistCreateSerializer(serializers.Serializer):
    artist_id = serializers.IntegerField()


class PlaylistSongCreateSerializer(serializers.Serializer):
    song_id = serializers.IntegerField()
