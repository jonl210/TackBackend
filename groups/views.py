from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render
from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import ProfileSerializer
from .models import Group

import random, string

#Create group with posted name
@api_view(['POST'])
def create_group(request):
    if request.method == "POST":
        name = request.POST["name"]
        profile = Profile.objects.get(user=request.user)
        u_id = generate_group_id()
        group = Group.objects.create(name=name, creator=profile, u_id=u_id)
        profile.groups.add(group)
        return Response({"message": "group created"})

#Add friend to a group
@api_view(['GET'])
def add_to_group(request, u_id):
    if request.method == "GET":
        username = request.query_params["name"]
        friend_profile = Profile.objects.get(
                         user=User.objects.get(username=username))
        group = Group.objects.get(u_id=u_id)
        friend_profile.joined_groups.add(group)
        group.members.add(friend_profile)
        return Response({"message": "friend added"})

@api_view(['GET'])
def remove_from_group(request, u_id):
    if request.method == "GET":
        username = request.query_params["name"]
        friend_profile = Profile.objects.get(
                         user=User.objects.get(username=username))
        group = Group.objects.get(u_id=u_id)
        friend_profile.joined_groups.remove(group)
        group.members.remove(friend_profile)
        return Response({"message": "friend removed"})

#Return members in group
@api_view(['GET'])
def members(request, u_id):
    if request.method == "GET":
        group = Group.objects.get(u_id=u_id)
        members = group.members.all()
        serializer = ProfileSerializer(members, many=True)
        return Response(serializer.data)

#Return friends not in group (specific to user making request)
@api_view(['GET'])
def non_members(request, u_id):
    if request.method == "GET":
        non_members = []

        profile = Profile.objects.get(user=request.user)
        group = Group.objects.get(u_id=u_id)
        friends = profile.friends.exclude(user=group.creator.user)
        members = group.members.all()

        if members.count() != 0:
            for member in members:
                friends = friends.exclude(user=member.user)

        for friend in friends:
            non_members.append(friend)

        serializer = ProfileSerializer(non_members, many=True)
        return Response(serializer.data)

#Generate unique group id
def generate_group_id():
    unique = False
    random_id = 0

    #Check if id already exists
    while not unique:
        random_id = ''.join([random.choice(string.ascii_letters +
            string.digits) for n in range(8)])

        if Group.objects.filter(u_id=random_id).exists():
            unique = False
        else:
            unique = True

    return random_id
