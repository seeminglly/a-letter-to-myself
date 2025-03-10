from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from .views import mypage

app_name = 'commons'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='commons/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name="signup"),
    path('mypage/', login_required(mypage), name='mypage'),
]
