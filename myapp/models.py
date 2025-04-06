from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

CATEGORIES = (
    ('past','과거'),
     ('today','오늘'),
     ('future','미래'),
)

MOOD_CHOICES = [
    ('happy', '기쁨'),
    ('sad', '슬픔'),
    ('angry', '분노'),
    ('worried', '불안'),
    ('neutral', '중립'),
]

def get_default_user():
    return User.objects.first().id  # ✅ 가장 첫 번째 사용자 ID를 기본값으로 설정
# Create your models here.
class Letters(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=get_default_user, related_name="letters") 
    id = models.AutoField(primary_key=True)  # 기본 키 설정
    title = models.CharField(max_length=200)  # 편지 제목
    content = models.TextField()  # 편지 내용
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    open_date = models.DateField()  # 편지를 열 수 있는 날짜 (선택)
    category = models.CharField(max_length=20,
                                choices=CATEGORIES,
                                default='future')
    emotion = models.CharField(max_length=30, choices=MOOD_CHOICES, null=True, blank=True)
    analyzed_at = models.DateTimeField(null=True, blank=True)
    # mood = models.CharField(max_length=10, choices=MOOD_CHOICES, default='happy')

    def save(self, *args, **kwargs):
        """ 개봉 일자에 따라 자동으로 카테고리 설정 """
        today = now().date()

        if self.open_date < today:
            self.category = 'past'  # 개봉일이 지났다면 과거
        elif self.open_date == today:
            self.category = 'today'  # 개봉일이 오늘이라면 오늘
        else:
            self.category = 'future'  # 개봉일이 아직 안 됐다면 미래

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.category}"
    

    
class LetterRoutine(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="routines")
    title = models.CharField(max_length=200, default="편지 루틴")  # 루틴 이름
    routine_type = models.CharField(max_length=10, choices=[('weekly', '매주'), ('monthly', '매월')],null=True, blank=True)  # ✅ 빈 값 허용)
    day_of_week = models.CharField(null=True, blank=True)  # 매주의 경우 요일 저장
    day_of_month = models.IntegerField(null=True, blank=True)
    time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    emotion = models.CharField(max_length=10, choices=MOOD_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.routine_type} ({self.day_of_week} {self.time})"
    
class SpecialDateRoutine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와 연결
    name = models.CharField(max_length=255)  # 기념일 이름 (ex. 생일, 결혼기념일 등)
    date = models.DateField()  # 기념일 날짜

    def __str__(self):
        return f"{self.user.username} - {self.name} ({self.date})"