from rest_framework import serializers
from .models import Tweet
from django.conf import settings


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']

    def validate_content(self, value):
        if len(value) > settings.MAX_TWEET_LENGTH:
            raise serializers.ValidationError("Tweet is over 240 chars!")
        return value
