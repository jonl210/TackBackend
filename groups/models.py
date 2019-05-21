from django.db import models
from datetime import datetime

#Group model
class Group(models.Model):
    name = models.CharField(max_length=60)
    creator = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="creator")
    u_id = models.CharField(max_length=8, default=0)
    members = models.ManyToManyField('users.profile', related_name="member")
    date = models.DateTimeField(default=datetime.now)
    posts = models.ManyToManyField('posts.post', related_name="group_posts")
