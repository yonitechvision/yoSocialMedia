from django.contrib import admin
from .models import Profile, Post, Like, Comment, Follower, Notification, Message, Repost, Hashtag, PostHashtag

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Repost)
admin.site.register(Hashtag)
admin.site.register(PostHashtag)
