
# Register your models here.
from django.contrib import admin
from .models import Letters, LetterRoutine

@admin.register(Letters)
class LettersAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'open_date', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'open_date')

@admin.register(LetterRoutine)
class LetterRoutineAdmin(admin.ModelAdmin):
    list_display = ('routine_type', 'day_of_week','day_of_month','time','title')
    list_filter = ('routine_type', 'day_of_week','day_of_month')

