from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    last_request = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "username"


class Like(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user} liked post {self.post})")


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = models.CharField(max_length=500)

    def __str__(self):
        return str(self.title)

