from django.urls import path
from auth_system import views

urlpatterns = [
    path('api/v1/token/create/', views.CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/v1/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token-obtain-refresh'),
    path('api/v1/logout/', views.logout_view, name='logout'),
]
