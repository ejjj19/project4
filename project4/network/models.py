from django.contrib.auth.models import AbstractUser, User
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=100, default="user", null=True , blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(max_length=100, null=True, blank=True)
    is_followed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="network/", default="network/profile.png",null=True)
    cover = models.ImageField(upload_to="network/", default="network/cover.png",null=True)
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.TextField(max_length=200, null=True)
    avatar = models.ImageField(upload_to="network/", default="",null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.post
    
class Like(models.Model):
    likes = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
    def __str__(self):
        return f"{self.follower} follows {self.following}"