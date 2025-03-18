from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from commons.forms import UserForm, ProfilePictureForm
from .forms import ProfilePictureForm
from django.shortcuts import render
from django.db.models import Count
from myapp.models import Letters
from .models import UserProfile

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ 사용자 저장 후, 반환된 객체 사용
            login(request, user)  # ✅ 자동 로그인
            return redirect('/')  # ✅ 회원가입 후 홈으로 이동
        else:
            # ✅ 회원가입 실패 시 오류 메시지 표시
            return render(request, 'commons/signup.html', {'form': form})
    else:
        form = UserForm()

    return render(request, 'commons/signup.html', {'form': form})
@login_required
def mypage(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    # context = {'profile_user':user, 'profile_type': 'base'}
    mood_counts = Letters.objects.filter(user=request.user).values("mood").annotate(count=Count("mood")).order_by("-count")
    # 가장 많이 기록된 감정 가져오기
    most_frequent_mood = mood_counts[0]["mood"] if mood_counts else None
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # ✅ 프로필이 없으면 자동 생성    

    context = {
        "user": request.user,
        "user_profile": user_profile,  # ✅ 프로필 사진을 템플릿으로 전달
        "mood_counts": mood_counts,
        "most_frequent_mood": most_frequent_mood,
    }
    return render(request, 'commons/mypage.html', context)

@login_required
def update_profile_picture(request):
    user_profile = request.user.userprofile  # ✅ 현재 사용자의 프로필 가져오기

    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("mypage")  # ✅ 변경 후 마이페이지로 이동

    else:
        form = ProfilePictureForm(instance=user_profile)

    return render(request, "myapp/update_profile_picture.html", {"form": form})