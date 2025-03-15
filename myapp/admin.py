
# Register your models here.
from django.contrib import admin
from .models import Letters, LetterRoutine, SpecialDateRoutine

@admin.register(Letters)
class LettersAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'open_date', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'open_date')

@admin.register(LetterRoutine)
class LetterRoutineAdmin(admin.ModelAdmin):
    list_display = ('user','routine_type', 'day_of_week','day_of_month','time','title')
    list_filter = ('user','routine_type', 'day_of_week','day_of_month')
    def save_model(self, request, obj, form, change):
        if not obj.user:  # 만약 user가 설정되지 않았다면
            obj.user = request.user  # 현재 로그인한 사용자로 자동 설정
        obj.save()

@admin.register(SpecialDateRoutine)
class SpecialDateRoutineAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_filter = ('name', 'date')

