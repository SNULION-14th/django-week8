from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers as rf_serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from .models import Artist, Song, SongArtist, Playlist, PlaylistSong, User
from .serializers import ArtistSerializer, SongSerializer, PlaylistSerializer, UserSerializer


# Artist
class ArtistListView(APIView):
    @extend_schema(
        summary="가수 목록 조회",
        description="가수 목록을 조회합니다.",
        responses={200: ArtistSerializer(many=True)},
    )
    def get(self, request):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="가수 생성",
        description="가수를 생성합니다.",
        request=inline_serializer(
            name="ArtistCreateRequest",
            fields={"name": rf_serializers.CharField()}
        ),
        responses={201: ArtistSerializer},
    )
    def post(self, request):
        name = request.data.get("name")
        if not name:
            return Response({"detail": "[name] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        artist = Artist.objects.create(name=name)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtistDetailView(APIView):
    @extend_schema(
        summary="가수 조회",
        description="특정 가수를 조회합니다.",
        responses={200: ArtistSerializer},
    )
    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="가수 수정",
        description="특정 가수를 수정합니다.",
        request=inline_serializer(
            name="ArtistUpdateRequest",
            fields={"name": rf_serializers.CharField()}
        ),
        responses={200: ArtistSerializer},
    )
    def put(self, request, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        name = request.data.get("name")
        if not name:
            return Response({"detail": "[name] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        artist.name = name
        artist.save()
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="가수 삭제",
        description="특정 가수를 삭제합니다.",
        responses={204: None},
    )
    def delete(self, request, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Song
class SongListView(APIView):
    @extend_schema(
        summary="노래 목록 조회",
        description="노래 목록을 조회합니다.",
        responses={200: SongSerializer(many=True)},
    )
    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="노래 생성",
        description="노래를 생성합니다.",
        request=inline_serializer(
            name="SongCreateRequest",
            fields={
                "title": rf_serializers.CharField(),
                "lowest_pitch": rf_serializers.CharField(),
                "highest_pitch": rf_serializers.CharField(),
            }
        ),
        responses={201: SongSerializer},
    )
    def post(self, request):
        title = request.data.get("title")
        lowest_pitch = request.data.get("lowest_pitch")
        highest_pitch = request.data.get("highest_pitch")
        if not title:
            return Response({"detail": "[title] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        if not lowest_pitch:
            return Response({"detail": "[lowest_pitch] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        if not highest_pitch:
            return Response({"detail": "[highest_pitch] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        song = Song.objects.create(title=title, lowest_pitch=lowest_pitch, highest_pitch=highest_pitch)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SongDetailView(APIView):
    @extend_schema(
        summary="노래 조회",
        description="특정 노래를 조회합니다.",
        responses={200: SongSerializer},
    )
    def get(self, request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="노래 수정",
        description="특정 노래를 수정합니다.",
        request=inline_serializer(
            name="SongUpdateRequest",
            fields={
                "title": rf_serializers.CharField(),
                "lowest_pitch": rf_serializers.CharField(),
                "highest_pitch": rf_serializers.CharField(),
            }
        ),
        responses={200: SongSerializer},
    )
    def put(self, request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        title = request.data.get("title")
        lowest_pitch = request.data.get("lowest_pitch")
        highest_pitch = request.data.get("highest_pitch")
        if not title or not lowest_pitch or not highest_pitch:
            return Response({"detail": "[title, lowest_pitch, highest_pitch] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        song.title = title
        song.lowest_pitch = lowest_pitch
        song.highest_pitch = highest_pitch
        song.save()
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="노래 삭제",
        description="특정 노래를 삭제합니다.",
        responses={204: None},
    )
    def delete(self, request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# User
class UserListView(APIView):
    @extend_schema(
        summary="회원 목록 조회",
        description="회원 목록을 조회합니다.",
        responses={200: UserSerializer(many=True)},
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="회원 생성",
        description="회원을 생성합니다.",
        request=inline_serializer(
            name="UserCreateRequest",
            fields={
                "name": rf_serializers.CharField(),
                "email": rf_serializers.EmailField(),
                "lowest_pitch": rf_serializers.CharField(),
                "highest_pitch": rf_serializers.CharField(),
            }
        ),
        responses={201: UserSerializer},
    )
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        lowest_pitch = request.data.get("lowest_pitch")
        highest_pitch = request.data.get("highest_pitch")
        if not name or not email or not lowest_pitch or not highest_pitch:
            return Response({"detail": "[name, email, lowest_pitch, highest_pitch] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(name=name, email=email, lowest_pitch=lowest_pitch, highest_pitch=highest_pitch)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    @extend_schema(
        summary="회원 조회",
        description="특정 회원을 조회합니다.",
        responses={200: UserSerializer},
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="회원 수정",
        description="특정 회원을 수정합니다.",
        request=inline_serializer(
            name="UserUpdateRequest",
            fields={
                "name": rf_serializers.CharField(),
                "email": rf_serializers.EmailField(),
                "lowest_pitch": rf_serializers.CharField(),
                "highest_pitch": rf_serializers.CharField(),
            }
        ),
        responses={200: UserSerializer},
    )
    def put(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        name = request.data.get("name")
        email = request.data.get("email")
        lowest_pitch = request.data.get("lowest_pitch")
        highest_pitch = request.data.get("highest_pitch")
        if not name or not email or not lowest_pitch or not highest_pitch:
            return Response({"detail": "[name, email, lowest_pitch, highest_pitch] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        user.name = name
        user.email = email
        user.lowest_pitch = lowest_pitch
        user.highest_pitch = highest_pitch
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="회원 삭제",
        description="특정 회원을 삭제합니다.",
        responses={204: None},
    )
    def delete(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Playlist
class PlaylistListView(APIView):
    @extend_schema(
        summary="플레이리스트 목록 조회",
        description="플레이리스트 목록을 조회합니다.",
        responses={200: PlaylistSerializer(many=True)},
    )
    def get(self, request):
        playlists = Playlist.objects.all()
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트 생성",
        description="플레이리스트를 생성합니다.",
        request=inline_serializer(
            name="PlaylistCreateRequest",
            fields={
                "name": rf_serializers.CharField(),
                "user_id": rf_serializers.IntegerField(),
            }
        ),
        responses={201: PlaylistSerializer},
    )
    def post(self, request):
        name = request.data.get("name")
        user_id = request.data.get("user_id")
        if not name or not user_id:
            return Response({"detail": "[name, user_id] fields missing."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        playlist = Playlist.objects.create(name=name, user=user)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlaylistDetailView(APIView):
    @extend_schema(
        summary="플레이리스트 조회",
        description="특정 플레이리스트를 조회합니다.",
        responses={200: PlaylistSerializer},
    )
    def get(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트 수정",
        description="특정 플레이리스트를 수정합니다.",
        request=inline_serializer(
            name="PlaylistUpdateRequest",
            fields={"name": rf_serializers.CharField()}
        ),
        responses={200: PlaylistSerializer},
    )
    def put(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        name = request.data.get("name")
        if not name:
            return Response({"detail": "[name] field missing."}, status=status.HTTP_400_BAD_REQUEST)
        playlist.name = name
        playlist.save()
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="플레이리스트 삭제",
        description="특정 플레이리스트를 삭제합니다.",
        responses={204: None},
    )
    def delete(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# SongArtist
class SongArtistView(APIView):
    @extend_schema(
        summary="노래에 가수 연결",
        description="노래에 가수를 연결합니다.",
        request=inline_serializer(
            name="SongArtistCreateRequest",
            fields={"artist_id": rf_serializers.IntegerField()}
        ),
        responses={201: None},
    )
    def post(self, request, song_id):
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        artist_id = request.data.get("artist_id")
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        SongArtist.objects.get_or_create(song=song, artist=artist)
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="노래에서 가수 제거",
        description="노래에서 가수를 제거합니다.",
        responses={204: None},
    )
    def delete(self, request, song_id, artist_id):
        try:
            sa = SongArtist.objects.get(song_id=song_id, artist_id=artist_id)
        except SongArtist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PlaylistSong
class PlaylistSongView(APIView):
    @extend_schema(
        summary="플레이리스트에 노래 추가",
        description="플레이리스트에 노래를 추가합니다.",
        request=inline_serializer(
            name="PlaylistSongCreateRequest",
            fields={"song_id": rf_serializers.IntegerField()}
        ),
        responses={201: None},
    )
    def post(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(pk=playlist_id)
        except Playlist.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        song_id = request.data.get("song_id")
        try:
            song = Song.objects.get(pk=song_id)
        except Song.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        PlaylistSong.objects.get_or_create(playlist=playlist, song=song)
        return Response(status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="플레이리스트에서 노래 제거",
        description="플레이리스트에서 노래를 제거합니다.",
        responses={204: None},
    )
    def delete(self, request, playlist_id, song_id):
        try:
            ps = PlaylistSong.objects.get(playlist_id=playlist_id, song_id=song_id)
        except PlaylistSong.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ps.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)