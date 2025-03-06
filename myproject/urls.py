"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # myapp의 URL 포함
    path('', views.home, name='home'),
    path('writing/', views.write_letter, name="writing"),
    path('postbox/', views.postbox, name='postbox'),
    path('letters/', views.letter_list, name='letter_list'),  # 작성한 편지 목록
    path('letters/past/', views.past_letters, name='past_letters'),  # ✅ 과거 편지 목록
    path('letters/today/', views.today_letters, name='today_letters'),  # ✅ 오늘 편지 목록
    path('letters/future/', views.future_letters, name='future_letters'),  # ✅ 미래 편지 목록
    path('routine/', views.routine, name="routine"),
]
