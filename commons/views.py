import json
from django.shortcuts import render,get_object_or_404

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import openai
import requests
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
from rest_framework.response import Response



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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def analyze_emotion_api(request):
    """최근 5개의 편지를 감정 분석하고, 감정별 통계와 가장 많은 감정 반환"""
    emotion_list = []
    user = request.user
    letters = Letters.objects.filter(user=user)

    try:
        for letter in letters:
            if letter.emotion:
                emotion_list.append(letter.emotion)
                continue

            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "너는 감정을 분석하는 AI야. 사용자가 쓴 여러 편지를 문맥과 단어 등을 고려하여 분석하고 감정을 무조건 happy, sad, angry, worried, neutral 중 하나로 나타내주세요"
                    },
                    {
                        "role": "user",
                        "content": letter.content
                    }
                ],
                max_tokens=7
            )
            emotion = response.choices[0].message.content.strip().lower()
            emotion_list.append(emotion)

            # 편지에 감정 결과 저장
            letter.emotion = emotion
            letter.analyzed_at = now()
            letter.save(update_fields=["emotion", "analyzed_at"])

    except openai.error.RateLimitError:
        return Response({"error": "현재 감정 분석 기능이 제한되어 있습니다. 나중에 다시 시도해주세요."}, status=429)

    # 감정 통계
    emotion_counts = dict(Counter(emotion_list))
    most_frequent = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None

    #json형태로 반환
    return Response({
        "emotions": emotion_counts,
        "most_frequent_mood": most_frequent
    }, status=200)


@api_view(["POST"])
def generate_comforting_message(request):
    """감정에 맞는 위로의 말 생성"""

    emotion = request.data.get("emotion")

    comfort_prompts = {
            "happy": "기분이 좋다니 정말 다행이에요! \n 당신의 행복이 오래 지속되기를 바라요. \n 당신의 기분이 오래 지속될 수 있도록 영화와 노래 추천을 해드릴게요!",
            "sad": "오늘 힘든 하루였군요. \n 저는 당신을 응원하고 있어요. \n당신은 혼자가 아니에요.",
            "angry": "화가 날 수도 있어요. \n하지만 깊게 호흡하고 긍정적인 방향으로 생각해보는 건 어떨까요?",
            "worried": "걱정이 많을 땐 작은 것부터 해결해 나가는 것이 중요해요.\n 천천히 하나씩 정리해봐요.",
            "diary": "어떤 감정이든 괜찮아요. \n오늘도 수고 많았어요!"
        }
    message = comfort_prompts.get(emotion, "당신의 감정을 이해하고 싶어요. 좀 더 이야기해 줄 수 있나요?")
    return Response({"comfort_message": message})


@api_view(["POST"])
def recommend_movies_and_music(request):
    """감정에 따라 적절한 영화와 음악을 추천하는 함수"""

    most_frequent_mood = request.data.get("most_frequent_mood")
    #emotion_counts = analyze_emotion_api(request._request)
    #most_frequent_mood = Counter(emotion_counts).most_common(1)[0][0]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"너는 감정을 기반으로 영화를 추천하는 AI야. '{most_frequent_mood}' 감정을 가진 사람에게 추천할 만한 대한민국이나 외국 영화 3개와 음악 3개의 제목과 관련 태그 정보를 알려주세요. 영화와 노래의 문단을 줄바꿈으로 나누고, 한 줄에 하나씩 적어주세요."},
            ],
            max_tokens=250
        )
        recommendation_text = response.choices[0].message.content
        return Response({"recommendations": recommendation_text})  # ✅ dict로 감싸기
    
    except openai.error.RateLimitError:
        return "현재 추천 기능이 제한되어 있습니다. 나중에 다시 시도해주세요."

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_emotion_summary(request):
    csrf_token = request.COOKIES.get('csrftoken')

    headers = {
        'X-CSRFToken': csrf_token
    }
    
    """마이페이지용 감정분석/메세지/추천 통합 api"""
    user = request.user
    BASE_URL = "http://127.0.0.1:8000/commons"


    # 1. 사용자 편지 감정 분석 api호출
    try:
        print("🚀 감정 분석 API 호출 시작")
        emotion_res = requests.post(
            f"{BASE_URL}/api/emotions/analyze/",
            headers=headers,
            cookies = request.COOKIES
        )
        emotion_data = emotion_res.json() #api응답을 json형태로 파싱
        emotions = emotion_data.get("emotions", {})
        most_frequent_mood = emotion_data.get("most_frequent_mood")
        print("✅ 감정 분석 결과:", emotion_res.status_code, emotion_res.text)
    except Exception as e:
        emotions = {}
        most_frequent_mood = None
        print("❌ 요청 실패:", e)

    # 2. 위로 메세지 api 호출
    try:
        print("🚀 위로 메시지 생성 API 호출 시작")
        msg_res = requests.post(
            f"{BASE_URL}/api/emotions/message/",
            headers=headers,
            json={"emotion": most_frequent_mood}
        )
        comfort_message = msg_res.json().get("comfort_message")
        print("✅ 위로 메시지 응답:", msg_res.status_code, msg_res.text)
    except Exception as e:
        comfort_message = "감정 기반 메세지를 불러올 수 없습니다."
        print("❌ 요청 실패:", e)
    
    # 3. 감정 기반 추천 api 호출
    try:
        print("🚀 추천 API 호출 시작")
        recommend_res = requests.post(
            f"{BASE_URL}/api/recommendations/emotion-based/",
            headers=headers,
            cookies = request.COOKIES
        )
        recommendations = recommend_res.json().get("recommendations")
        print("✅ 추천 결과:", recommend_res.status_code, recommend_res.text)
    except Exception as e:
        recommendations = "추천 결과를 불러올 수 없습니다."
        print("❌ 요청 실패:", e)
    
    return Response({
        "emotions": emotions,
        "most_frequent_mood": most_frequent_mood,
        "comfort_message": comfort_message,
        "recommendations": recommendations,
    })


@login_required
def mypage(request):
    user = request.user
    # 🔗 내부 API 통합 호출
    BASE_URL = "http://127.0.0.1:8000/commons"  # 배포 시 도메인으로 변경
    try:
        response = requests.get(
            f"{BASE_URL}/api/user/emotion-summary/",
            cookies=request.COOKIES  # 세션 인증 유지
        )
        if response.status_code == 200:
            data = response.json()
            emotions = data.get("emotions", {})
            most_frequent_mood = data.get("most_frequent_mood")
            comfort_message = data.get("comfort_message")
            recommendations = data.get("recommendations")
        else:
            emotions = {}
            most_frequent_mood = None
            comfort_message = "감정 메시지를 불러오지 못했습니다."
            recommendations = "추천 결과를 불러오지 못했습니다."
    except Exception as e:
        emotions = {}
        most_frequent_mood = None
        comfort_message = "감정 메시지를 불러오지 못했습니다."
        recommendations = "추천 결과를 불러오지 못했습니다."
    # 사용자 정보
    profile, _ = Profile.objects.get_or_create(user=user)
    user_profile, _ = UserProfile.objects.get_or_create(user=user)
    letter_count = user.letters.count()
    routine_count = user.routines.count()

    # # 1. 편지 가져오기
    # letters = Letters.objects.filter(user=request.user)

    #  # 감정 분석 결과 저장 (최대 1회만 실행)
    # emotions = analyze_emotion_api(request)

   

    # # 실패 여부 체크
    # is_emotion_failed = emotions and any("제한되어 있습니다" in e for e in emotions)


    # # 감정 분석 실패 여부에 따라 처리 분기
    # if is_emotion_failed:
    #     most_frequent_mood = None
    #     comfort_message = emotions[0]
    #     recommendations = "영화/음악 추천도 사용할 수 없습니다."
    #     mood_counts = []  # 차트용 데이터도 비워줘야 함
    # else:
    #     mood_counts = Counter(emotions) #감정 빈도 계산
    #     most_frequent_mood = mood_counts.most_common(1)[0][0] if mood_counts else None
    #     comfort_message = generate_comforting_message(most_frequent_mood)
    #     recommendations = recommend_movies_and_music(most_frequent_mood)


   
    # # 감정에 따른 위로 메시지 및 추천 영화/음악 생성
    # if most_frequent_mood:
    #     comfort_message = generate_comforting_message(most_frequent_mood)
    #     recommendations = recommend_movies_and_music(most_frequent_mood)
    # else:
    #     comfort_message = "아직 감정 분석된 편지가 없습니다."
    #     recommendations = "편지를 작성하면 감정 분석 후 추천 영화와 음악을 제공해 드립니다."
        
    
    # user = request.user
    # letter_count = user.letters.count()  # related_name을 활용
    # routine_count = user.routines.count()

    # print("닉네임:", profile.nickname)
    # print("소개:", profile.bio)
    # Django 템플릿으로 데이터 전달
    context = {
        "user": user,
        "user_profile": user_profile,
        "profile": profile,
        "emotions": json.dumps(emotions),
        "mood_counts": emotions,
        "most_frequent_mood": most_frequent_mood,
        "comfort_message": comfort_message,
        "recommendations": recommendations,
        "letter_count": letter_count,
        "routine_count": routine_count,
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