from rest_framework import serializers
from django.contrib.auth.models import User

#Serialize to test sign up data
class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

#Serialize data to return user searched for
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',)
