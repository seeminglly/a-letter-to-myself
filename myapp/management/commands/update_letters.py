from django.core.management.base import BaseCommand
from myapp.models import Letter
from django.utils.timezone import now

class Command(BaseCommand):
    help = "편지 개봉 날짜 도래 시 상태 업데이트"

    def handle(self, *args, **kwargs):
        today = now().date()
        letters = Letter.objects.filter(open_date=today, category='future')

        for letter in letters:
            letter.update_category_and_status()
            self.stdout.write(self.style.SUCCESS(f"Updated {letter.title} to 'today'"))

