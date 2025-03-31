from celery import shared_task
from django.core.mail import send_mail
from .models import LetterRoutine
from django.utils.timezone import now
from django.conf import settings


@shared_task
def send_letter_reminders():
    today = now().strftime("%A")  # 현재 요일 (Monday, Tuesday 등)
    current_day = now().day  # 오늘 날짜 (1~31)
    current_time = now().time()

    routines = LetterRoutine.objects.filter(time=current_time)

    for routine in routines:
        # 매주 선택한 경우 (요일 매칭)
        if routine.routine_type == 'weekly' and routine.day_of_week == today:
            send_notification(routine)

        # 매월 선택한 경우 (날짜 매칭)
        if routine.routine_type == 'monthly' and routine.day_of_month == current_day:
            send_notification(routine)

def send_notification(routine):
    send_mail(
        subject="📩 편지 작성 알림",
        message=f"{routine.user.username}님! 오늘은 편지를 작성할 날입니다. ({routine.time})",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[routine.user.email],
        fail_silently=False
    )
