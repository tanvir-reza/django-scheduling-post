# Import Model and Serializer from Django Rest Framework
from rest_framework import serializers
from .models import UserManagement, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManagement
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response["author"]:
            response['author'] = instance.author.first_name
            response['author_id'] = instance.author.id
        return response
