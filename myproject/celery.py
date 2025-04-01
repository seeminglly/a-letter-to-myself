import os
from celery.schedules import crontab
from celery import Celery

# Django 세팅 연결
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

# Django settings 가져오기
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

#한국 시간 설정
app.conf.timezone = 'Asia/Seoul'
app.conf.enable_utc = False

# Celery Beat 스케줄 설정
app.conf.beat_schedule = {
    'send-routine-reminder-every-hour': {
        'task': 'myapp.tasks.send_letter_reminders',
        'schedule': crontab(minute='*/1'),  # 매 1분마다 실행
    },
}
