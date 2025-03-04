from django.shortcuts import render
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView,LoginView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from app.serializers import UserSerializer

# Create your views here.

@api_view(['GET'])
def index(request):
    return render(request, 'index.html')

class CustomLoginView(LoginView):
    
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        user = self.user
        user_serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "user": user_serializer.data  # Corrected this line
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomRegisterView(RegisterView):
    

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")
        email = request.data.get("email")
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")
        fullname = request.data.get("fullname")
        # Check if fields are empty or not
        if username == '':
            return Response({"message": "Username is required"}, status=status.HTTP_200_OK)
        
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            return Res onse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if api_settings.USE_JWT:
            self.access_token, self.refresh_token = jwt_encode(user)
        elif not api_settings.SESSION_LOGIN:
            api_settings.TOKEN_CREATOR(self.token_model, user, serializer)
        return user
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):
    return Response("All posts")