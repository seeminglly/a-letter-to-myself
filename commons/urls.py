from django.urls import path
from django.contrib.auth import views as auth_views
#from django.contrib.auth.decorators import login_required
from . import views
from .views import mypage, update_profile
from .views import (
    user_emotion_summary,         # 통합 마이페이지 API
    analyze_emotion_api,          # 감정 분석
    generate_comforting_message,  # 위로 메시지
    recommend_movies_and_music    # 추천 API
)
from django.conf import settings
from django.conf.urls.static import static


app_name = 'commons'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name="signup"),
    path('mypage/', mypage, name='mypage'),
    path("api/emotions/analyze/", analyze_emotion_api, name="analyze-emotion"),
    path("api/emotions/message/", generate_comforting_message, name="comfort-msg"),
    path("api/recommendations/emotion-based/", recommend_movies_and_music, name="recommend"),
    path("api/user/emotion-summary/", user_emotion_summary, name="emotion-summary"),
    path("update-profile/", update_profile, name="update_profile"),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
