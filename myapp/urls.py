from django.urls import path, include
from .views import letter_list, letter_json
from django.contrib.auth import views as auth_views
from myapp import views


urlpatterns = [
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
    
    path('signup/', views.signup, name='signup'),
]


