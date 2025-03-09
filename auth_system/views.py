from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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
                samesite='Lax'
            )
            response.data.pop('access', None)
            response.data.pop('refresh', None)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            set_access_cookie(response, access_token)
            response.data.pop('access', None)
            print("Token Refreshed")
        return response


def set_access_cookie(response, access_cookie):
    response.set_cookie(
        key='access_token',
        value=access_cookie,
        httponly=True,
        secure=True,
        samesite='Lax',
        path='/',
    )


@api_view(['POST'])
def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')

    if refresh_token:
        token = RefreshToken(refresh_token)
        token.blacklist()

    response = Response({"logged_out": True})
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response
