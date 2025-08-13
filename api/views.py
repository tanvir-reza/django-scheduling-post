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
from app.serializers import UserSerializer, PostSerializer
from app.models import Post, UserManagement
import time
from rest_framework import viewsets


# Create your views here.

@api_view(['GET'])
def index(request):
    posts = Post.objects.all()

    for post in posts:
        print(post.author.username)

    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

class CustomLoginView(LoginView):
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username == '' or password == '':
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        try:
            self.serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"message": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
        self.login()
        user = self.user
        user_serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        data = {
            "message": "User logged in successfully",
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
        if username == None:
            return Response({"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        if password1 == None or password2 == None:
            return Response({"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if len(username) < 4:
                return Response({"message": "Username must be at least 4 characters"}, status=status.HTTP_400_BAD_REQUEST)
            if password1 != password2:
                return Response({"message": "Password do not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": "User registered successfully",
            },
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data),
        )

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if api_settings.USE_JWT:
            self.access_token, self.refresh_token = jwt_encode(user)
        elif not api_settings.SESSION_LOGIN:
            api_settings.TOKEN_CREATOR(self.token_model, user, serializer)
        return user
    
# make refresh token function view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    data = {
        "message": "Token refreshed successfully",
        "access_token": str(access_token),
        "refresh_token": str(refresh),
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def authors(request):
    authors = UserManagement.objects.all()

    serializer = UserSerializer(authors, many=True)

    return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    title = request.data.get("title")
    description = request.data.get("description")
    if title == None or description == None:
        return Response({"message": "Title and description are required"}, status=status.HTTP_400_BAD_REQUEST)
    # get file from request
    image = request.FILES.get("image")
    try:
        data = data = request.data
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    return Response("Post created successfully")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_posts(request):
    my_posts = Post.objects.filter(author=request.user)
    serializer = PostSerializer(my_posts, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    post = Post.objects.get(id=pk)
    title = request.data.get("title")
    description = request.data.get("description")
    if title == None or description == None:
        return Response({"message": "Title and description are required"}, status=status.HTTP_400_BAD_REQUEST)
    post.title = title
    post.description = description
    auth = UserManagement.objects.get(id=request.data.get("author"))
    post.author = auth
    post.save()
    return Response("Post updated successfully")

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response("Post deleted successfully")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({"message": "User logged out successfully"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_details(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def aiView(request):
    user_data = request.data.get("user_data")
    if user_data == None:
        return Response({"message": "User data is required"}, status=status.HTTP_400_BAD_REQUEST)
    from transformers import pipeline

    classifier = pipeline('sentiment-analysis')
    result = classifier('I hate you so much')
    print(result)
    return Response({"message": result}, status=status.HTTP_200_OK)