from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, UTC
from django_faceblog import settings


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Call the original post method to get the token data
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            set_access_cookie(response, access_token)
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                expires=datetime.now(UTC) + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            )
            response.data.pop('access', None)
            response.data.pop('refresh', None)
        return response


class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response("Error getting the token", status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"message": "Access Token Refreshed"}, status=status.HTTP_200_OK)
            set_access_cookie(response=response, access_token=access_token)
        except InvalidToken:
            return Response({"Error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        return response


def set_access_cookie(response, access_token):
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='None',
        expires=datetime.now(UTC) + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
    )


@api_view(['POST'])
def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()

    response = Response({"logged_out": True})
    # Delete access token
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,
        samesite="None",
        expires=0,
    )
    return response
