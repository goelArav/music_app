from django.contrib import admin

# Register your models here.


from django.contrib import admin

from .models import Genre, Musician, Post, Comment

admin.site.register(Genre)
admin.site.register(Musician)
admin.site.register(Post)
admin.site.register(Comment)