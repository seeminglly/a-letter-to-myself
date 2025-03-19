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
    path('commons/', include('commons.urls')),
    path('', views.home, name='home'),
    path('writing/', views.write_letter, name="writing"),
    path('postbox/', views.postbox, name='postbox'),
    path('letters/', views.letter_list, name='letter_list'),  # 작성한 편지 목록
    path('routine/', views.save_routine , name="routine"),
    path('accounts/', include('django.contrib.auth.urls')),  
   
]
