from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    birthday = models.DateField(auto_now=False)
    blog_url = models.URLField(max_length = 60, blank=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ 사용자와 1:1 연결
    profile_picture = models.ImageField(upload_to="profile_pics/", default="default.jpg")  # ✅ 프로필 사진 저장

    def __str__(self):
        return self.user.username