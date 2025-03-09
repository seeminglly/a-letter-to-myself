from django.urls import path, include
from .views import letter_list, letter_json
from django.contrib.auth import views as auth_views
from myapp import views

app_name = 'commons'
urlpatterns = [
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
    path('commons/', include('commons.urls', namespace='commons')),  # ✅ 네임스페이스 추가
]


