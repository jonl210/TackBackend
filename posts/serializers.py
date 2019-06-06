from rest_framework import serializers
from .models import Post

from datetime import datetime

#Display posted by username
class ByField(serializers.Field):
    def to_representation(self, value):
        return value.user.username

#Display group name
class GroupName(serializers.Field):
    def to_representation(self, value):
        return value.name

#Display date field
class DateField(serializers.Field):
    def to_representation(self, value):
        return value.strftime("%b %-d, %Y")

class PostSerializer(serializers.ModelSerializer):
    by = ByField()
    group = GroupName()
    date = DateField()

    class Meta:
        model = Post
        fields = ('url', 'u_id', 'caption', 'date', 'by', 'group',)
