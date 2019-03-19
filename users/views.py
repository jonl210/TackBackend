from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import RegisterFormSerializer, UserSerializer
from friendrequests.models import FriendRequest
from groups.models import Group
from groups.serializers import TableGroupSerializer

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
            user_search_profile = Profile.objects.get(user=User.objects.get(username=query))
            profile = Profile.objects.get(user=request.user)
            serializer = UserSerializer(user_search_profile.user)

            #Check if friend request exists or if already friends of if same user
            if FriendRequest.objects.filter(from_user=profile,to_user=user_search_profile).exists():
                return Response({"user": serializer.data,"message": "request pending"})
            elif profile.friends.all().filter(user=user_search_profile.user).exists():
                return Response({"user": serializer.data, "message": "already friends"})
            elif profile == user_search_profile:
                return Response({"user": serializer.data, "message": "you"})

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

#Get all users groups
@api_view(['GET'])
def groups(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        created_groups = profile.groups.all()
        joined_groups = profile.joined_groups.all()
        created_group_serializer = TableGroupSerializer(created_groups, many=True)
        joined_group_serializer = TableGroupSerializer(joined_groups, many=True)
        return Response({"created_groups": created_group_serializer.data,
                         "joined_groups": joined_group_serializer.data})
