from django.urls import path
from rest_framework import routers

from posts import views

router = routers.DefaultRouter()
router.register(prefix=r'post', viewset=views.PostViewSet, basename="posts")
router.register(prefix=r'post-likes', viewset=views.LikePostViewSet, basename="post-likes")
router.register(prefix=r'post-comments', viewset=views.CommentViewSet, basename="post-comments")

urlpatterns = [

]

urlpatterns += router.urls

