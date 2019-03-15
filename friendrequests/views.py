from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import FriendRequest
from users.models import Profile

#Send friend request to user
@api_view(['POST'])
def send_friend_request(request, username):
    if request.method == "POST":
        from_user = Profile.objects.get(user=request.user)
        to_user = Profile.objects.get(user=User.objects.get(username=username))
        friend_request = FriendRequest.objects.create(from_user=from_user,
                                                      to_user=to_user,)
        to_user.friend_requests.add(friend_request)
        return Response({"message": "request sent"})

#Add friend and delete request
@api_view(['GET'])
def accept_friend_request(request, username):
    if request.method == "GET":
        from_profile = Profile.objects.get(user=User.objects.get(username=username))
        to_profile = Profile.objects.get(user=request.user)
        to_profile.friends.add(from_profile)
        FriendRequest.objects.get(from_user=from_profile, to_user=to_profile).delete()
        return Response({"message": "friend request accepted"})

#Delete request
@api_view(['GET'])
def delete_friend_request(request, username):
    if request.method == "GET":
        from_profile = Profile.objects.get(user=User.objects.get(username=username))
        to_profile = Profile.objects.get(user=request.user)
        FriendRequest.objects.get(from_user=from_profile, to_user=to_profile).delete()
        return Response({"message": "friend request deleted"})
