from django.contrib import admin
from basic_app.models import Profile, User, Friendship, Comment, Post, TempFriendRequest

# Register your models here.
admin.site.register(Friendship)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(TempFriendRequest)

