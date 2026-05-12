from django.contrib import admin
from .models import TodoList, Calendar, Routine  



admin.site.register(TodoList)
admin.site.register(Calendar)
admin.site.register(Routine)