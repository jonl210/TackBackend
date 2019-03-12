from django.db import models

#Friend request model
class FriendRequest(models.Model):
    from_user = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="from_user")
    to_user = models.ForeignKey('users.profile', on_delete=models.CASCADE, related_name="to_user")
    from_user_username = models.CharField(max_length=30, default="placeholder")
