from rest_framework import serializers


class ArtistRequestSerializer(serializers.Serializer):
    name = serializers.CharField()


class SongRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    lowest_pitch = serializers.CharField()
    highest_pitch = serializers.CharField()


class UserRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    lowest_pitch = serializers.CharField()
    highest_pitch = serializers.CharField()


class PlaylistRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    user_id = serializers.IntegerField()


class SongArtistRequestSerializer(serializers.Serializer):
    artist_id = serializers.IntegerField()


class PlaylistSongRequestSerializer(serializers.Serializer):
    song_id = serializers.IntegerField()
