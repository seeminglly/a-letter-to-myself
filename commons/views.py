import json
from django.shortcuts import render,get_object_or_404

# Create your views here.
import openai
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from commons.forms import UserForm, ProfileForm, ProfilePictureForm
from .forms import ProfilePictureForm
from django.shortcuts import render
from collections import Counter  
# from django.db.models import Count
from myapp.models import Letters
from .models import Profile, UserProfile
import os
from dotenv import load_dotenv
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    print("🛠 login_view 호출됨")  # ✅ 무조건 호출 여부 확인

    if request.method == "POST":
        print("🔑 POST 요청 수신됨")
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"✅ 로그인 성공: {user.username}")
            login(request, user)
            return redirect('/')
        else:
            print("❌ 로그인 실패: 인증 실패")
            return render(request, 'commons/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
    
    return render(request, 'commons/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ 사용자 저장 후, 반환된 객체 사용

            Profile.objects.create(user=user)  # 새로운 Profile 객체 생성
            UserProfile.objects.get_or_create(user=user)  # 새로운 UserProfile 객체 생성 및 연결

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



def analyze_emotion(letters):
    """사용자가 작성한 편지를 감정 분석하여 감정을 반환"""
    emotion_list = []

    try:
        for letter in letters:
            if letter.emotion:  # 이미 분석된 경우
                emotion_list.append(letter.emotion)
                continue
             
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "너는 감정을 분석하는 AI야. 사용자가 쓴 여러 편지를 문맥과 단어 등을 고려하여 분석하고 감정을 무조건 happy, sad, angry, worried, neutral 중 하나로 나타내주세요"},
                    {"role": "user", "content": letter.content}
                ],
                max_tokens=7
            )
            emotion = response.choices[0].message.content.strip().lower()
            emotion_list.append(emotion)
            letter.emotion = emotion
            letter.analyzed_at = now()
            letter.save(update_fields=["emotion", "analyzed_at"])  # DB에 저장

    except openai.error.RateLimitError:
            return ["현재 감정 분석 기능이 제한되어 있습니다. 나중에 다시 시도해주세요."]
  # ✅ 감정별 횟수 딕셔너리 반환
    emotion_counts = dict(Counter(emotion_list))
    return emotion_counts


def generate_comforting_message(emotion):
    """감정에 맞는 위로의 말 생성"""
    comfort_prompts = {
        "happy": "기분이 좋다니 정말 다행이에요! \n 당신의 행복이 오래 지속되기를 바라요. \n 당신의 기분이 오래 지속될 수 있도록 영화와 노래 추천을 해드릴게요!",
        "sad": "오늘 힘든 하루였군요. \n 저는 당신을 응원하고 있어요. \n당신은 혼자가 아니에요.",
        "angry": "화가 날 수도 있어요. \n하지만 깊게 호흡하고 긍정적인 방향으로 생각해보는 건 어떨까요?",
        "worried": "걱정이 많을 땐 작은 것부터 해결해 나가는 것이 중요해요.\n 천천히 하나씩 정리해봐요.",
        "diary": "어떤 감정이든 괜찮아요. \n오늘도 수고 많았어요!"
    }
    return comfort_prompts.get(emotion, "당신의 감정을 이해하고 싶어요. 좀 더 이야기해 줄 수 있나요?")

def recommend_movies_and_music(emotion):
    """감정에 따라 적절한 영화와 음악을 추천하는 함수"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"너는 감정을 기반으로 영화를 추천하는 AI야. '{emotion}' 감정을 가진 사람에게 추천할 만한 대한민국이나 외국 영화 3개와 음악 3개의 제목과 관련 태그 정보를 알려주세요. 영화와 노래의 문단을 줄바꿈으로 나누고, 한 줄에 하나씩 적어주세요."},
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except openai.error.RateLimitError:
        return "현재 추천 기능이 제한되어 있습니다. 나중에 다시 시도해주세요."


@login_required
def mypage(request):
    """사용자가 작성한 편지를 감정 분석하고 위로의 말과 추천 영화/음악을 반환하는 API"""
    
     # ✅ 프로필 정보 최신 상태로 가져오기
    profile, _ = Profile.objects.get_or_create(user=request.user)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # 1. 편지 가져오기
    letters = Letters.objects.filter(user=request.user)

     # 감정 분석 결과 저장 (최대 1회만 실행)
    emotions = analyze_emotion(letters)

   

    # 실패 여부 체크
    is_emotion_failed = emotions and any("제한되어 있습니다" in e for e in emotions)


    # 감정 분석 실패 여부에 따라 처리 분기
    if is_emotion_failed:
        most_frequent_mood = None
        comfort_message = emotions[0]
        recommendations = "영화/음악 추천도 사용할 수 없습니다."
        mood_counts = []  # 차트용 데이터도 비워줘야 함
    else:
        mood_counts = Counter(emotions) #감정 빈도 계산
        most_frequent_mood = mood_counts.most_common(1)[0][0] if mood_counts else None
        comfort_message = generate_comforting_message(most_frequent_mood)
        recommendations = recommend_movies_and_music(most_frequent_mood)


    # # 사용자의 모든 편지 불러오기
    # user_letters = Letters.objects.filter(user=request.user).order_by("-created_at")
    # # 감정별 편지 개수 계산 (통계)
    #mood_counts = user_letters.values("mood").annotate(count=Count("mood")).order_by("-count")

    # # 가장 많이 나타난 감정 확인
    # most_frequent_mood = order_mood_counts[0]["response"] if mood_counts else None

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

    print("닉네임:", profile.nickname)
    print("소개:", profile.bio)
    # Django 템플릿으로 데이터 전달
    context = {
        "user": request.user,
        "user_profile": user_profile,
        "profile" : profile,
        "user_profile": user_profile,
        #"user_letters": user_letters,  # 사용자의 모든 편지 리스트
        "emotions": json.dumps(emotions),
        "mood_counts": mood_counts,  # 감정 통계 데이터
        "is_emotion_failed": is_emotion_failed,
        "most_frequent_mood": most_frequent_mood,  # 가장 많이 나타난 감정
        "comfort_message": comfort_message,  # 위로 메시지
        "recommendations": recommendations, # 추천 영화 & 음악
        'letter_count': letter_count,
        'routine_count':routine_count
    }

    return render(request, 'commons/mypage.html', context)

@login_required
def update_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid() and picture_form.is_valid():
            profile = profile_form.save(commit=False)  # ✅ 수정 전 저장 중지
            profile.user = request.user                # ✅ 필요한 경우 수동 연결
            profile.save()                             # ✅ 수동 저장

            picture_form.save()
            return redirect('commons:mypage')

        else:
            print(profile_form.errors)  # 오류 출력
            print(picture_form.errors)
    else:
        profile_form = ProfileForm(instance=profile)
        picture_form = ProfilePictureForm(instance=user_profile)

    context = {
        'profile_form': profile_form,
        'picture_form': picture_form,
        'profile': profile,
        'user_profile': user_profile
    }
    return render(request, 'commons/update_profile.html', context)