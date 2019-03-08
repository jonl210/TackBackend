from django.db import models
from django.contrib.auth.models import User

#User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
