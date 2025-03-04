# Import Model and Serializer from Django Rest Framework
from rest_framework import serializers
from .models import UserManagement, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = '__all__'
