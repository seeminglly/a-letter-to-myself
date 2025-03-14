from django.urls import path, include
from .views import letter_list, letter_json, save_routine, save_specialDateRoutine
from django.contrib.auth import views as auth_views
from myapp import views


urlpatterns = [
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
    path('api/routines/', views.get_routine_events, name='get_routine_events'),
    path("save_routine/", save_routine, name = "routine"),
    path('signup/', views.signup, name='signup'),
    path('save_specialDateRoutine/', save_specialDateRoutine, name="save_specialDateRoutine" )
]


