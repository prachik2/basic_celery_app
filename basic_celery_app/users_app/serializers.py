from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'linked_in_url', 'twitter_url', 'blog_url', 'status']


class EditUserSerializer(serializers.ModelSerializer):

    user_id = serializers.CharField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'linked_in_url', 'twitter_url', 'blog_url', 'status')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
