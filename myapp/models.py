from django.db import models

CATEGORIES = (
    ('past','과거'),
     ('today','오늘'),
     ('tomorrow','미래')
)
# Create your models here.
class Letters(models.Model):
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