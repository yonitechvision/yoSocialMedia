from rest_framework import serializers
from .models import Post, Profile, Follower, Notification, Like, Comment, Message, Repost, Hashtag, PostHashtag
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'profile_picture', 'location', 'website', 'cover_photo']

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = serializers.StringRelatedField(many=True, read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)
    hashtags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author', 'timestamp', 'media', 'likes', 'comments', 'hashtags']

    def validate_media(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size should not exceed 5 MB.")
        if not value.name.endswith(('.jpg', '.png', '.mp4', '.pdf', '.docx')):
            raise serializers.ValidationError("Unsupported file format.")
        return value

# Like Serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created']

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created']

# Follower Serializer
class FollowerSerializer(serializers.ModelSerializer):
    user_from = UserSerializer(read_only=True)
    user_to = UserSerializer(read_only=True)

    class Meta:
        model = Follower
        fields = ['user_from', 'user_to', 'created']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'sender', 'notification_type', 'post', 'timestamp', 'is_read']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp']

# Repost Serializer
class RepostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Repost
        fields = ['id', 'user', 'post', 'created']

# Hashtag Serializer
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'name']

# PostHashtag Serializer
class PostHashtagSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    hashtag = HashtagSerializer(read_only=True)

    class Meta:
        model = PostHashtag
        fields = ['post', 'hashtag']

