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
    class Meta:
        model = Post
        fields = ("id", "title", "body")


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ("created_at", "post", "id", "user")

    def validate_post(self, value):
        if Like.objects.filter(post=value, user=self.context["request"].user).exists():
            raise serializers.ValidationError()
        return value


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data.get("username"),
            email=validated_data.get("email"),
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ("password", "username", "email", "id")
