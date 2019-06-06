from django.db import models
from datetime import datetime

#Post model
class Post(models.Model):
    url = models.URLField()
    u_id = models.CharField(max_length=11, default=0)
    caption = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    by = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="by")
    group = models.ForeignKey('groups.group', on_delete=models.CASCADE, related_name="group")
    favorites = models.ManyToManyField('favorites.Favorite', related_name="favorites")
