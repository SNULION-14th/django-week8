from django.urls import path
from .views import (
    SongListView, SongDetailView,
    ArtistListView, ArtistDetailView,
    UserListView, UserDetailView,
    PlaylistListView, PlaylistDetailView,
    SongArtistView, PlaylistSongView,
)

urlpatterns = [
    # Song
    path("songs/", SongListView.as_view()),
    path("songs/<int:song_id>/", SongDetailView.as_view()),

    # Artist
    path("artists/", ArtistListView.as_view()),
    path("artists/<int:artist_id>/", ArtistDetailView.as_view()),

    # User
    path("users/", UserListView.as_view()),
    path("users/<int:user_id>/", UserDetailView.as_view()),

    # Playlist
    path("playlists/", PlaylistListView.as_view()),
    path("playlists/<int:playlist_id>/", PlaylistDetailView.as_view()),

    # SongArtist
    path("songs/<int:song_id>/artists/", SongArtistView.as_view()),
    path("songs/<int:song_id>/artists/<int:artist_id>/", SongArtistView.as_view()),

    # PlaylistSong
    path("playlists/<int:playlist_id>/songs/", PlaylistSongView.as_view()),
    path("playlists/<int:playlist_id>/songs/<int:song_id>/", PlaylistSongView.as_view()),
]