from django.urls import path
from auth_system import views

urlpatterns = [
    path('token/create/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token-obtain-refresh'),
    path('logout/', views.logout_view, name='logout'),
]
