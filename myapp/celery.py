from celery.schedules import crontab
from celery import Celery

app = Celery('myapp')

app.conf.beat_schedule = {
    'send-routine-reminder-every-hour': {
        'task': 'myapp.tasks.send_letter_reminders',
        'schedule': crontab(minute=0, hour='*'),  # 매시간 0분마다 실행
    },
}
