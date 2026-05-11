# ./post/admin.py

from django.contrib import admin
from .models import Post, Exhibition, Log, Photo

admin.site.register(Post)
admin.site.register(Exhibition)
admin.site.register(Log)
admin.site.register(Photo)