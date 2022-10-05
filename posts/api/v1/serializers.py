from rest_framework import serializers

from posts.models import Post, Like, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username", "last_login", "last_request")


class AnalyticSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ("created_at", "total_likes")


class PostSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = ("id", "user", "title", "body", "total_likes")


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("user", "created_at", "post")


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        return user

    class Meta:
        model = UserProfile
        fields = ("password", "username", "email", "id")
