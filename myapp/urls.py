from django.urls import path, include
from .views import letter_list, letter_json, save_routine,delete_routine, get_routine_events
from django.contrib.auth import views as auth_views
from myapp import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'myapp'

urlpatterns = [
    path('index/', views.home, name="home"),
    path('letters/', letter_list, name='letter_list'),
    path('api/letters/<int:letter_id>/', letter_json, name='letter_json'),  # 편지 상세 API
    path('api/routines/', views.get_routine_events, name='get_routine_events'),
    path("routine/",save_routine, name = "save_routine"),
    path("routine/delete/<int:pk>/", delete_routine, name="delete_routine"),  # 루틴 삭제
    path('signup/', views.signup, name='signup'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)