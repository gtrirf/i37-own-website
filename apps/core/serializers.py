from rest_framework import serializers
from .models import MainInfo, Career, SocialLink


class MainInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainInfo
        fields = ['id', 'name', 'photo', 'text']


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'name', 'logo', 'created_at']


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'app', 'url']
