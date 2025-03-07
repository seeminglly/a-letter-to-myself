from django.db import models
from django.contrib.auth.models import User

CATEGORIES = (
    ('past','과거'),
     ('today','오늘'),
     ('future','미래'),
)
# Create your models here.
class Letters(models.Model):
    id = models.AutoField(primary_key=True)  # 기본 키 설정
    title = models.CharField(max_length=200)  # 편지 제목
    content = models.TextField()  # 편지 내용
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    open_date = models.DateField(null=True, blank=True)  # 편지를 열 수 있는 날짜 (선택)
    category = models.CharField(max_length=20,
                                choices=CATEGORIES,
                                default='오늘')
    
    def __str__(self):
        return self.title
    
class LetterRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    routine_type = models.CharField(max_length=10, choices=[('weekly', '매주'), ('monthly', '매월')])
    day_of_week = models.CharField(max_length=10, null=True, blank=True)  # 매주의 경우 요일 저장
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.routine_type} ({self.day_of_week} {self.time})"