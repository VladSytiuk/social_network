from django.contrib import admin

from posts.models import Like, Post, UserProfile

admin.site.register(Like)
admin.site.register(Post)
admin.site.register(UserProfile)
