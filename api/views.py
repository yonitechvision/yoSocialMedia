from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Profile, Post, Follower, Notification, Like, Comment, Message, Repost, Hashtag, PostHashtag
)
from .serializers import (
    UserSerializer, ProfileSerializer, PostSerializer, FollowerSerializer, NotificationSerializer,
    LikeSerializer, CommentSerializer, MessageSerializer, RepostSerializer, HashtagSerializer, PostHashtagSerializer
)
from django.db.models import Count

# User Sign-Up API View
class SignUpView(APIView):
    permission_classes = [AllowAny]  # Allow non-authenticated users to sign up

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if username or email is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        # Automatically create a profile for the new user
        Profile.objects.create(user=user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

# User ViewSet (CRUD for users)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Profile ViewSet
class ProfileViewSet(viewsets.ModelViewSet):
    #queryset = Profile.objects.all()
    queryset = Profile.objects.all().order_by('user__username')  # Order by username or another field
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Associate the profile with the authenticated user
        serializer.save(user=self.request.user)

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Enable file uploads

    def perform_create(self, serializer):
        # Automatically link the author to the authenticated user
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def feed(self, request):
        followed_users = Follower.objects.filter(user_from=request.user).values_list('user_to', flat=True)
        posts = Post.objects.filter(author__in=followed_users)

        # Sorting by date or popularity (likes)
        sort_by = request.query_params.get('sort_by', 'date')
        if sort_by == 'date':
            posts = posts.order_by('-timestamp')
        elif sort_by == 'popularity':
            posts = posts.annotate(like_count=Count('likes')).order_by('-like_count')

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

# Like ViewSet
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.request.data['post'])
            # Prevent double likes by the same user
            if Like.objects.filter(user=self.request.user, post=post).exists():
                return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

            # Create notification
            Notification.objects.create(
                user=post.author, sender=self.request.user,
                notification_type='like', post=post
            )
            serializer.save(user=self.request.user)

        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.request.data['post'])
            # Create notification for the comment
            Notification.objects.create(
                user=post.author, sender=self.request.user,
                notification_type='comment', post=post
            )
            serializer.save(user=self.request.user)

        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

# Follower ViewSet
class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def follow(self, request):
        user_to_follow = User.objects.get(id=request.data['user_to'])
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if Follower.objects.filter(user_from=request.user, user_to=user_to_follow).exists():
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        Follower.objects.create(user_from=request.user, user_to=user_to_follow)
        Notification.objects.create(user=user_to_follow, sender=request.user, notification_type='follow')
        return Response({'status': 'You are now following this user'})

    @action(detail=False, methods=['post'])
    def unfollow(self, request):
        user_to_unfollow = User.objects.get(id=request.data['user_to'])
        follow_relation = Follower.objects.filter(user_from=request.user, user_to=user_to_unfollow).first()
        if follow_relation:
            follow_relation.delete()
            return Response({'status': 'You have unfollowed this user'})
        return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)

# Notification Views
class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({'message': 'Notification marked as read'}, status=200)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)



# Message ViewSet

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')  # Order messages by timestamp
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Require authentication to access

    def perform_create(self, serializer):
        # Debug: Check incoming request data
        print("Incoming request data:", self.request.data)  # Debugging line to print incoming data

        # Extract the recipient ID from the request data
        recipient_id = self.request.data.get('recipient')
        
        # Check if recipient ID is provided
        if recipient_id is None:
            raise serializers.ValidationError("Recipient ID is required.")

        # Check if the recipient exists
        if not User.objects.filter(id=recipient_id).exists():
            raise serializers.ValidationError("Recipient does not exist.")

        # Retrieve the recipient User object
        recipient = User.objects.get(id=recipient_id)

        # Save the message with the sender and recipient
        serializer.save(sender=self.request.user, recipient=recipient)

    def get_queryset(self):
        """
        Optionally restricts the returned messages to a given user.
        """
        user = self.request.user
        # Return messages sent by or received by the authenticated user
        return Message.objects.filter(sender=user).union(Message.objects.filter(recipient=user)).order_by('-timestamp')


# Repost ViewSet
class RepostViewSet(viewsets.ModelViewSet):
    queryset = Repost.objects.all()
    serializer_class = RepostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.request.data['post'])
        serializer.save(user=self.request.user, post=post)

# Hashtag ViewSet
class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [IsAuthenticated]

# Trending Posts
class TrendingPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trending_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        serializer = PostSerializer(trending_posts, many=True)
        return Response(serializer.data)

