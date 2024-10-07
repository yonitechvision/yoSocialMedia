from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProfileViewSet, PostViewSet, FollowerViewSet, LikeViewSet, CommentViewSet,
    NotificationListView, MarkNotificationReadView, MessageViewSet, RepostViewSet, HashtagViewSet,
    TrendingPostView, SignUpView
)
from django.urls import path, include

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('posts', PostViewSet)
router.register('followers', FollowerViewSet)
router.register('likes', LikeViewSet)
router.register('comments', CommentViewSet)
router.register('messages', MessageViewSet)
router.register('reposts', RepostViewSet)
router.register('hashtags', HashtagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('posts/trending/', TrendingPostView.as_view(), name='trending-posts'),
]

