from django.db import models
from django.contrib.auth.models import User

from friendrequests.models import FriendRequest

#User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friend_requests = models.ManyToManyField(FriendRequest)
