
# Register your models here.
from django.contrib import admin
from .models import Letters

@admin.register(Letters)
class LettersAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'open_date', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'open_date')

