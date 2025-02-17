from rest_framework import routers

from users import views

router = routers.DefaultRouter()
routes = router.register(prefix='profile', viewset=views.ProfileViewSet, basename='profile')

urlpatterns = [

]

urlpatterns += router.urls