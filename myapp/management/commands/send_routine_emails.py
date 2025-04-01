from django.core.management.base import BaseCommand
from myapp.tasks import send_letter_reminders

class Command(BaseCommand):
    help = '정해진 루틴 시간에 맞는 유저에게 이메일 알림을 보냅니다.'

    def handle(self, *args, **kwargs):
        send_letter_reminders()
        self.stdout.write(self.style.SUCCESS('이메일 알림 전송 완료!'))