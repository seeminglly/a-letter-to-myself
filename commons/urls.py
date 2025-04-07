from django.urls import path
from django.contrib.auth import views as auth_views
#from django.contrib.auth.decorators import login_required
from . import views
from .views import mypage, update_profile, login_view
from django.conf import settings
from django.conf.urls.static import static


app_name = 'commons'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name="signup"),
    # path('mypage/', login_required(mypage), name='mypage'),
    path('mypage/', mypage, name='mypage'),
    path("update-profile/", update_profile, name="update_profile"),
    

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
