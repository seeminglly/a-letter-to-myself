from django.urls import path
from .views import letter_list, letter_json

urlpatterns = [
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
]
