from django.urls import path
from .views import (
    SongListView, SongDetailView,
    ArtistListView, ArtistDetailView,
    UserListView, UserDetailView,
    PlaylistListView, PlaylistDetailView,
    SongArtistCreateView, SongArtistDetailView,
    PlaylistSongCreateView, PlaylistSongDetailView,
)

urlpatterns = [
    path("songs/", SongListView.as_view()),
    path("songs/<int:song_id>/", SongDetailView.as_view()),
    path("artists/", ArtistListView.as_view()),
    path("artists/<int:artist_id>/", ArtistDetailView.as_view()),
    path("users/", UserListView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),
    path("playlists/", PlaylistListView.as_view()),
    path("playlists/<int:playlist_id>/", PlaylistDetailView.as_view()),
    path("songs/<int:song_id>/artists/", SongArtistCreateView.as_view()),
    path("songs/<int:song_id>/artists/<int:artist_id>/", SongArtistDetailView.as_view()),
    path("playlists/<int:playlist_id>/songs/", PlaylistSongCreateView.as_view()),
    path("playlists/<int:playlist_id>/songs/<int:song_id>/", PlaylistSongDetailView.as_view()),
]
