from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views
from .views import mypage, update_profile
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import login_view  # ✅ 이렇게 myapp에서 가져오기

app_name = 'commons'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name="signup"),
    # path('mypage/', login_required(mypage), name='mypage'),
    path('mypage/', mypage, name='mypage'),
    path("update-profile/", update_profile, name="update_profile"),
    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
