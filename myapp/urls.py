from django.urls import path, include
from .views import letter_list, letter_json, save_routine,get_routine_events
from django.contrib.auth import views as auth_views
from myapp import views
app_name = 'myapp'

urlpatterns = [
    path('index/', views.home, name="home"),
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
    path('api/routines/', views.get_routine_events, name='get_routine_events'),
    path("routine/",save_routine, name = "save_routine"),
    path('signup/', views.signup, name='signup'),
    path("api/routines/", get_routine_events, name="get_routine_events"), 
]


