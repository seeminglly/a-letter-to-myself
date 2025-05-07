from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os

# Create your models here.
from django.conf import settings
# Create your models here.

def profile_picture_upload_to(instance, filename):
    # 파일명을 slugify로 변환하여 안전한 문자로 만듬
    base, ext = os.path.splitext(filename)
    slugified_name = slugify(base)
    return f'profile_pics/{slugified_name}{ext}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(blank=True)
    picture = models.ImageField(blank=True)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    blog_url = models.URLField(max_length = 60, blank=True)
    
    def __str__(self):
        return self.user.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ✅ 사용자와 1:1 연결
    profile_picture = models.ImageField(
    upload_to='profile_pics/',
    blank=True,
    null=True
)
 # ✅ 프로필 사진 저장

    def __str__(self):
        return self.user.username
    

class RecommendationFeedback(models.Model):
        FEEDBACK_CHOICES = [
            ('like', '좋아요'),
            ('dislike', '별로예요')
        ]

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        item_type = models.CharField(max_length=20)  # 'movie' 또는 'music'
        item_title = models.CharField(max_length=255)
        feedback = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.user.username} - {self.item_type} - {self.feedback}"
        
        # models.py
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_title = models.TextField()
    item_type = models.CharField(max_length=10)  # 'movie' or 'music'
    feedback = models.CharField(max_length=10)  # 'like' or 'dislike'
    created_at = models.DateTimeField(auto_now_add=True)
