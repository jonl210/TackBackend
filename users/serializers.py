from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile

#Return count for model field
class ModelFieldCount(serializers.Field):
    def to_representation(self, value):
        return value.count()

#Serialize to test sign up data
class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

#Serialize user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)

#Return user serializer and basic profile info
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user',)

#Serialize profile with more data for profile tab
class ProfileTabSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friends = ModelFieldCount()
    groups = ModelFieldCount()
    joined_groups = ModelFieldCount()

    class Meta:
        model = Profile
        fields = ('user', 'friends', 'groups', 'joined_groups',)
