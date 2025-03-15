from django.db import models
from django.contrib.auth.models import User

CATEGORIES = (
    ('past','과거'),
     ('today','오늘'),
     ('future','미래'),
)

MOOD_CHOICES = [
    ('happy', '😊 행복'),
    ('sad', '😢 슬픔'),
    ('angry', '😡 화남'),
    ('worried', '🤔 고민'),
]


# Create your models here.
class Letters(models.Model):
    id = models.AutoField(primary_key=True)  # 기본 키 설정
    title = models.CharField(max_length=200)  # 편지 제목
    content = models.TextField()  # 편지 내용
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    open_date = models.DateField()  # 편지를 열 수 있는 날짜 (선택)
    category = models.CharField(max_length=20,
                                choices=CATEGORIES,
                                default='오늘')
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='diary')
    
    def __str__(self):
        return self.title
    
class LetterRoutine(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="편지 루틴")  # 루틴 이름
    routine_type = models.CharField(max_length=10, choices=[('weekly', '매주'), ('monthly', '매월')],null=True, blank=True)  # ✅ 빈 값 허용)
    day_of_week = models.CharField(null=True, blank=True)  # 매주의 경우 요일 저장
    day_of_month = models.IntegerField(null=True, blank=True)
    time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.routine_type} ({self.day_of_week} {self.time})"
    
class SpecialDateRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결
    name = models.CharField(max_length=255)  # 기념일 이름 (ex. 생일, 결혼기념일 등)
    date = models.DateField()  # 기념일 날짜

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.date})"