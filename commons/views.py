from django.shortcuts import render,get_object_or_404

# Create your views here.
import openai
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from commons.forms import UserForm, ProfilePictureForm
from .forms import ProfilePictureForm
from django.shortcuts import render
from django.db.models import Count
from myapp.models import Letters
from .models import UserProfile
import os

from dotenv import load_dotenv


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

load_dotenv()

# .env에서 API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")



def analyze_emotion(letter):
    """사용자가 작성한 편지를 감정 분석하여 감정을 반환"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 감정을 분석하는 AI야. 사용자의 편지를 문맥과 단어 등을 고려하여 분석하고 감정을 happy, sad, angry, worried, neutral 중 하나로 분류해."},
            {"role": "user", "content": letter}
        ],
        max_tokens=10
    )
    return response.choices[0].message.content.strip().lower()

def generate_comforting_message(emotion):
    """감정에 맞는 위로의 말 생성"""
    comfort_prompts = {
        "happy": "기분이 좋다니 정말 다행이에요! 당신의 행복이 오래 지속되기를 바라요. \n 당신의 기분이 오래 지속될 수 있도록 영화와 노래 추천을 해드릴게요!",
        "sad": "오늘 힘든 하루였군요. 저는 당신을 응원하고 있어요. 당신은 혼자가 아니에요.",
        "angry": "화가 날 수도 있어요. 하지만 깊게 호흡하고 긍정적인 방향으로 생각해보는 건 어떨까요?",
        "worried": "걱정이 많을 땐 작은 것부터 해결해 나가는 것이 중요해요. 천천히 하나씩 정리해봐요.",
        "diary": "어떤 감정이든 괜찮아요. 오늘도 수고 많았어요!"
    }
    return comfort_prompts.get(emotion, "당신의 감정을 이해하고 싶어요. 좀 더 이야기해 줄 수 있나요?")

def recommend_movies_and_music(emotion):
    """감정에 따라 적절한 영화와 음악을 추천하는 함수"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"너는 감정을 기반으로 영화를 추천하는 AI야. '{emotion}' 감정을 가진 사람에게 추천할 만한 영화 3개와 음악 3개의 제목과 관련 태그 정보를 알려주세요. 영화와 노래의 문단을 줄바꿈으로 나누고, 한 줄에 하나씩 적어주세요."},
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except openai.error.RateLimitError:
        return "현재 추천 기능이 제한되어 있습니다. 나중에 다시 시도해주세요."

@login_required
def mypage(request):
    """사용자가 작성한 편지를 감정 분석하고 위로의 말과 추천 영화/음악을 반환하는 API"""
    
    # 사용자 프로필 불러오기
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    # 가장 많이 기록된 감정 가져오기
    mood_counts = Letters.objects.filter(user=request.user).values("mood").annotate(count=Count("mood")).order_by("-count")
    most_frequent_mood = mood_counts[0]["mood"] if mood_counts else None

    # 사용자의 모든 편지 불러오기
    user_letters = Letters.objects.filter(user=request.user).order_by("-created_at")
    # 감정별 편지 개수 계산 (통계)
    mood_counts = user_letters.values("mood").annotate(count=Count("mood")).order_by("-count")

    # 가장 많이 나타난 감정 확인
    most_frequent_mood = mood_counts[0]["mood"] if mood_counts else None

    # 감정에 따른 위로 메시지 및 추천 영화/음악 생성
    if most_frequent_mood:
        comfort_message = generate_comforting_message(most_frequent_mood)
        recommendations = recommend_movies_and_music(most_frequent_mood)
    else:
        comfort_message = "아직 감정 분석된 편지가 없습니다."
        recommendations = "편지를 작성하면 감정 분석 후 추천 영화와 음악을 제공해 드립니다."

    user = request.user
    letter_count = user.letters.count()  # related_name을 활용
    routine_count = user.routines.count()
    # Django 템플릿으로 데이터 전달
    context = {
        "user": request.user,
        "user_profile": user_profile,
        "user_letters": user_letters,  # 사용자의 모든 편지 리스트
        "mood_counts": mood_counts,  # 감정 통계 데이터
        "most_frequent_mood": most_frequent_mood,  # 가장 많이 나타난 감정
        "comfort_message": comfort_message,  # 위로 메시지
        "recommendations": recommendations, # 추천 영화 & 음악
        'letter_count': letter_count,
        'routine_count':routine_count
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