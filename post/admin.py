from django.contrib import admin


from .models import Artist, Song, SongArtist, User, Playlist, PlaylistSong

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(SongArtist)
admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)