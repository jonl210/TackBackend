from django.db import models
from datetime import datetime

#Favorite model
class Favorite(models.Model):
    profile = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="profile")
    post = models.ForeignKey('posts.post', on_delete=models.CASCADE, related_name="post")
    date = models.DateTimeField(default=datetime.now)
