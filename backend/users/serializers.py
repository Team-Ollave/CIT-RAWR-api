from rest_framework import serializers

from .choices import UserType
from .models import User, UserProfile


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    profile_data = UserProfileModelSerializer(read_only=True, source="profile")

    class Meta:
        model = User
        fields = ("id", "email", "user_type", "profile", "profile_data")


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserQuerySerializer(serializers.Serializer):
    user_type = serializers.CharField(required=False)

    def validate(self, attrs):
        if (user_type := attrs.get("user_type")) and user_type not in UserType.values:
            raise serializers.ValidationError("user_type value is invalid.")

        return attrs
