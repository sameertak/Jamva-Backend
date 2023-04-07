from rest_framework import serializers
from .models import userModel

class userDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=15)
    profile = serializers.ImageField(default='profile.png')

