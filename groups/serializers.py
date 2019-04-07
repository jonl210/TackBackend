from rest_framework import serializers
from .models import Group

#Display creator username
class CreatorField(serializers.Field):
    def to_representation(self, value):
        return value.user.username

#Serialize group to display in table
class TableGroupSerializer(serializers.ModelSerializer):
    creator = CreatorField()

    class Meta:
        model = Group
        fields = ('name', 'date', 'creator', 'u_id',)
