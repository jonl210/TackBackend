from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import RegisterFormSerializer, UserSerializer
from friendrequests.models import FriendRequest

#Sign up new user
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    if request.method == "POST":
        serializer = RegisterFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            new_user = User.objects.create_user(username, email, password)
            Token.objects.create(user=new_user)
            Profile.objects.create(user=new_user)
            return Response({"message": "user created"})

#Search for a user
@api_view(['GET'])
def user_search(request):
    if request.method == "GET":
        query = request.query_params["searchquery"]
        if User.objects.filter(username=query).exists():
            user_search_result = User.objects.get(username=query)
            serializer = UserSerializer(user_search_result)
            return Response(serializer.data)
        else:
            return Response({"message": "user does not exist"})

#User inbox
@api_view(['GET'])
def inbox(request):
    if request.method == "GET":
        user_requests = []
        profile = Profile.objects.get(user=request.user)
        friend_requests = profile.friend_requests.all()

        #Get from_user from each request to serialize
        for request in friend_requests:
            user_requests.append(request.from_user.user)

        serializer = UserSerializer(user_requests, many=True)
        return Response(serializer.data)
