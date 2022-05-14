from rest_framework import serializers

from profiles_api import models


class SearchSerializer(serializers.Serializer):
    """Serializes a keyword field of APIView"""
    keyword = serializers.CharField(max_length=200)


class UserDataSerializer(serializers.Serializer):
    """Serializer favorites, voted fields of UserProfile"""
    # {'favorite' : int, 'voted' : {'id' : int}}
    favorite = serializers.IntegerField()
    voted = serializers.JSONField()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = (
            'id',
            'user_profile',
            'createdAt',
            'contentContributorId',
            'contentContributorScore',
            'contentTitle',
            'popularityName',
            'popularityValue',
            'sourceName',
            'sourceOrder',
            'sourceUrl',
            'vote',
        )
        extra_kwargs = {'user_profile': {'read_only': True}}
