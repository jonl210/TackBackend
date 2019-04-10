from rest_framework import serializers
from .models import Group

from datetime import datetime

#Display creator username
class CreatorField(serializers.Field):
    def to_representation(self, value):
        return value.user.username

class DateField(serializers.Field):
    def to_representation(self, value):
        return value.strftime("%b %-d %Y")

#Serialize group to display in table
class GroupSerializer(serializers.ModelSerializer):
    creator = CreatorField()
    date = DateField()

    class Meta:
        model = Group
        fields = ('name', 'date', 'creator', 'u_id',)
