from django.urls import path
from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register(r'user/posts', views.PostViewSet)

urlpatterns = [
    path('posts/', views.UserFollowingPostsListAPIView.as_view(), name='user_following_posts'),
]

urlpatterns += router.urls

