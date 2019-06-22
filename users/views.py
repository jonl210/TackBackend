from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import RegisterFormSerializer, ProfileSerializer, ProfileTabSerializer
from friendrequests.models import FriendRequest
from groups.models import Group
from groups.serializers import GroupSerializer
from posts.serializers import PostSerializer
from favorites.models import Favorite

#Sign up new user
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    if request.method == "POST":
        serializer = RegisterFormSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data["username"]
            email = serializer.validated_data["email"]

            if ' ' in username:
                return Response({"message": "space in username"})

            if User.objects.filter(username=username).exists():
                return Response({"message": "username in use"})

            if User.objects.filter(email=email).exists():
                return Response({"message": "email in use"})

            password = serializer.validated_data["password"]
            new_user = User.objects.create_user(username, email, password)
            Token.objects.create(user=new_user)
            Profile.objects.create(user=new_user)
            return Response({"message": "user created"})

#Return user's profile
@api_view(['GET'])
def profile(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        profile_serializer = ProfileTabSerializer(profile)
        return Response(profile_serializer.data)

#Return user's friends
@api_view(['GET'])
def friends(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        friends = profile.friends.all()
        serializer = ProfileSerializer(friends, many=True)
        return Response(serializer.data)

#Search for a user
@api_view(['GET'])
def user_search(request):
    if request.method == "GET":
        query = request.query_params["search_query"]
        if User.objects.filter(username=query).exists():
            user_search_profile = Profile.objects.get(user=User.objects.get(username=query))
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(user_search_profile)

            #Check if friend request exists or if already friends of if same user
            if FriendRequest.objects.filter(from_user=profile,to_user=user_search_profile).exists():
                return Response({"data": serializer.data, "message": "request pending"})
            elif profile.friends.all().filter(user=user_search_profile.user).exists():
                return Response({"data": serializer.data, "message": "already friends"})
            elif profile == user_search_profile:
                return Response({"data": serializer.data, "message": "you"})

            return Response({"data": serializer.data, "message": "can request"})
        else:
            return Response({"message": "user does not exist"})

#Return user's friend requests
@api_view(['GET'])
def inbox(request):
    if request.method == "GET":
        user_requests = []
        profile = Profile.objects.get(user=request.user)
        friend_requests = profile.friend_requests.all()

        #Get from_user from each request to serialize
        for request in friend_requests:
            user_requests.append(request.from_user)

        serializer = ProfileSerializer(user_requests, many=True)
        return Response(serializer.data)

#Get users's created groups
@api_view(['GET'])
def created_groups(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        created_groups = profile.groups.all()
        created_group_serializer = GroupSerializer(created_groups, many=True)
        return Response(created_group_serializer.data)

#Get user's joined groups
@api_view(['GET'])
def joined_groups(request):
    if request.method == "GET":
        profile = Profile.objects.get(user=request.user)
        joined_groups = profile.joined_groups.all()
        joined_groups_serializer = GroupSerializer(joined_groups, many=True)
        return Response(joined_groups_serializer.data)

#Get posts user has favorited
@api_view(['GET'])
def favorites(request):
    if request.method == "GET":
        favorited_posts = []
        profile = Profile.objects.get(user=request.user)
        sorted_favorites = Favorite.objects.filter(profile=profile).order_by("-date")

        for favorite in sorted_favorites:
            favorited_posts.append(favorite.post)

        serializer = PostSerializer(favorited_posts, many=True)
        return Response(serializer.data)
