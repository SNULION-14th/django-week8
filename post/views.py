from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Artist, Song, SongArtist, Playlist, PlaylistSong, User
from .serializers import (
    ArtistSerializer,
    PlaylistSerializer,
    PlaylistSongCreateSerializer,
    SongArtistCreateSerializer,
    SongSerializer,
    UserSerializer,
)


@extend_schema_view(
    get=extend_schema(summary="가수 목록 조회", responses={200: ArtistSerializer(many=True)}),
    post=extend_schema(summary="가수 생성", request=ArtistSerializer, responses={201: ArtistSerializer}),
)
class ArtistListView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


@extend_schema_view(
    get=extend_schema(summary="가수 조회", responses={200: ArtistSerializer}),
    put=extend_schema(summary="가수 수정", request=ArtistSerializer, responses={200: ArtistSerializer}),
    patch=extend_schema(summary="가수 부분 수정", request=ArtistSerializer, responses={200: ArtistSerializer}),
    delete=extend_schema(summary="가수 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    lookup_url_kwarg = "artist_id"


@extend_schema_view(
    get=extend_schema(summary="노래 목록 조회", responses={200: SongSerializer(many=True)}),
    post=extend_schema(summary="노래 생성", request=SongSerializer, responses={201: SongSerializer}),
)
class SongListView(generics.ListCreateAPIView):
    serializer_class = SongSerializer

    def get_queryset(self):
        return Song.objects.prefetch_related("songartist_set__artist")


@extend_schema_view(
    get=extend_schema(summary="노래 조회", responses={200: SongSerializer}),
    put=extend_schema(summary="노래 수정", request=SongSerializer, responses={200: SongSerializer}),
    patch=extend_schema(summary="노래 부분 수정", request=SongSerializer, responses={200: SongSerializer}),
    delete=extend_schema(summary="노래 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class SongDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SongSerializer
    lookup_url_kwarg = "song_id"

    def get_queryset(self):
        return Song.objects.prefetch_related("songartist_set__artist")


@extend_schema_view(
    get=extend_schema(summary="회원 목록 조회", responses={200: UserSerializer(many=True)}),
    post=extend_schema(summary="회원 생성", request=UserSerializer, responses={201: UserSerializer}),
)
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema_view(
    get=extend_schema(summary="회원 조회", responses={200: UserSerializer}),
    put=extend_schema(summary="회원 수정", request=UserSerializer, responses={200: UserSerializer}),
    patch=extend_schema(summary="회원 부분 수정", request=UserSerializer, responses={200: UserSerializer}),
    delete=extend_schema(summary="회원 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "user_id"


@extend_schema_view(
    get=extend_schema(summary="플레이리스트 목록 조회", responses={200: PlaylistSerializer(many=True)}),
    post=extend_schema(summary="플레이리스트 생성", request=PlaylistSerializer, responses={201: PlaylistSerializer}),
)
class PlaylistListView(generics.ListCreateAPIView):
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.select_related("user").prefetch_related("playlistsong_set__song__songartist_set__artist")


@extend_schema_view(
    get=extend_schema(summary="플레이리스트 조회", responses={200: PlaylistSerializer}),
    put=extend_schema(summary="플레이리스트 수정", request=PlaylistSerializer, responses={200: PlaylistSerializer}),
    patch=extend_schema(summary="플레이리스트 부분 수정", request=PlaylistSerializer, responses={200: PlaylistSerializer}),
    delete=extend_schema(summary="플레이리스트 삭제", responses={204: OpenApiResponse(description="삭제 완료")}),
)
class PlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaylistSerializer
    lookup_url_kwarg = "playlist_id"

    def get_queryset(self):
        return Playlist.objects.select_related("user").prefetch_related("playlistsong_set__song__songartist_set__artist")


class SongArtistCreateView(generics.GenericAPIView):
    serializer_class = SongArtistCreateSerializer

    @extend_schema(
        summary="노래에 가수 연결",
        request=SongArtistCreateSerializer,
        responses={201: OpenApiResponse(description="연결 완료")},
    )
    def post(self, request, song_id):
        song = get_object_or_404(Song, pk=song_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        artist = get_object_or_404(Artist, pk=serializer.validated_data["artist_id"])
        SongArtist.objects.get_or_create(song=song, artist=artist)
        return Response(status=status.HTTP_201_CREATED)


class SongArtistDetailView(generics.GenericAPIView):
    @extend_schema(summary="노래에서 가수 제거", responses={204: OpenApiResponse(description="삭제 완료")})
    def delete(self, request, song_id, artist_id):
        song_artist = get_object_or_404(SongArtist, song_id=song_id, artist_id=artist_id)
        song_artist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistSongCreateView(generics.GenericAPIView):
    serializer_class = PlaylistSongCreateSerializer

    @extend_schema(
        summary="플레이리스트에 노래 추가",
        request=PlaylistSongCreateSerializer,
        responses={201: OpenApiResponse(description="추가 완료")},
    )
    def post(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        song = get_object_or_404(Song, pk=serializer.validated_data["song_id"])
        PlaylistSong.objects.get_or_create(playlist=playlist, song=song)
        return Response(status=status.HTTP_201_CREATED)


class PlaylistSongDetailView(generics.GenericAPIView):
    @extend_schema(summary="플레이리스트에서 노래 제거", responses={204: OpenApiResponse(description="삭제 완료")})
    def delete(self, request, playlist_id, song_id):
        playlist_song = get_object_or_404(PlaylistSong, playlist_id=playlist_id, song_id=song_id)
        playlist_song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
