from django.db import models
from django.contrib.auth.models import User

from friendrequests.models import FriendRequest
from groups.models import Group
from posts.models import Post

#User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_requests = models.ManyToManyField(FriendRequest)
    friends = models.ManyToManyField("self")
    groups = models.ManyToManyField(Group, related_name="my_groups")
    joined_groups = models.ManyToManyField(Group, related_name="joined_groups")
    posts = models.ManyToManyField(Post, related_name="my_posts")
    favorites = models.ManyToManyField(Post, related_name="favorited_posts")
