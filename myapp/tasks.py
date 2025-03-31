from celery import shared_task
from django.core.mail import send_mail
from .models import LetterRoutine
from django.utils.timezone import now, localtime
from django.conf import settings
from datetime import timedelta

@shared_task
def send_letter_reminders():
    now_dt = localtime(now()).replace(second=0, microsecond=0)
    today = now_dt.strftime("%A")  # 현재 요일 (Monday, Tuesday 등)
    current_day = now_dt.day  # 오늘 날짜 (1~31)
    current_time = now_dt.time()

    # ±1분 오차 허용
    window_start = (now_dt - timedelta(minutes=1)).time()
    window_end = (now_dt + timedelta(minutes=1)).time()
    
    print("✅ 루틴 알림 작업 실행됨!")
    print(f"현재 시간: {current_time}")
    print(f"알림 시간 범위: {window_start} ~ {window_end}")
    print(f"오늘 요일: {today}, 날짜: {current_day}")
    
    routines = LetterRoutine.objects.filter(time__range=(window_start, window_end))

    for routine in routines:
        # 매주 선택한 경우 (요일 매칭)
        print(f"🔍 루틴 체크: {routine.routine_type} / {routine.day_of_week} / {routine.time}")
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
    print(f"📬 알림 전송 완료 → {routine.user.email}")
