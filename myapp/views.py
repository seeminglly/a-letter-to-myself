from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import Letters, LetterRoutine, SpecialDateRoutine
from myapp.forms import LetterForm,SpecialDateRoutineForm
from commons.forms import UserForm
from django.utils.timezone import now  # 현재 날짜 가져오기
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


# Create your views here.
def home(request):
    return render(request, 'myapp/index.html')

# 1️⃣ 편지 작성 뷰
def write_letter(request):
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():
            letter = form.save(commit=False)  # ✅ 데이터 저장 전에 추가 설정
            letter.user = request.user  # 🔥 작성자를 현재 로그인한 사용자로 설정
            letter.category = 'future' # 기본적으로 미래 카테고리로 분류
            letter.save()
            return redirect('letter_list')  # 편지 목록 페이지로 이동
    else:
        form = LetterForm()
        
    return render(request, 'myapp/writing.html', {'form': form})


# 2️⃣ 작성된 편지 목록 보기
@login_required(login_url='commons:login') #로그인 안 하면 로그인 페이지로 이동
def letter_list(request):
    letters = Letters.objects.filter(user=request.user)


    today = datetime.now().date()
    
    for letter in letters:
        if letter.open_date == today:
            letter.category = 'today'
        elif letter.open_date > today:
            letter.category = 'future'
        else:
            letter.category = 'past'
    
    letter.save()  # ✅ DB에 저장!


    return render(request, 'myapp/letter_list.html', {
        'letters': letters,
    })


#개별 편지 상세보기api
@login_required
def letter_json(request, letter_id):
    letter = get_object_or_404(Letters, id=letter_id)
    data = {
        'id':letter.id,
        'title': letter.title,
        'content': letter.content,
        'letter_date': letter.open_date.strftime("%Y-%m-%d"), #개봉 가능 날짜
    }
    return JsonResponse(data)

#편지 루틴 만들기
@login_required(login_url='commons:login')
@csrf_exempt
def save_routine(request):
    days = range(1, 32)
    routine = None  # ✅ 기본값 설정
    special_routine = None  # ✅ 기본값 설정

    if "title" in request.POST:
        title = request.POST.get("title") or "기본 루틴 제목"
        routine_type = request.POST.get("routine_type")
        day_of_week = request.POST.get("day_of_week") if routine_type == "weekly" else None
        day_of_month = request.POST.get("day_of_month") if routine_type == "monthly" else None
        time = request.POST.get("routine_time")

        routine = LetterRoutine.objects.create(
            user=request.user,
            title=title,
            routine_type=routine_type,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            time=time
        )

    elif "name" in request.POST:
        name = request.POST.get("name")
        date = request.POST.get("date")

        special_routine = SpecialDateRoutine.objects.create(
            user=request.user,
            name=name,
            date=date
        )

    # ✅ 내 루틴 보기
    routines = LetterRoutine.objects.filter(user=request.user)
    specialDays = SpecialDateRoutine.objects.filter(user=request.user)

    lists = {
        "days": days,
        "routines": routines,
        "specialDays": specialDays,
        "routine_id": routine.id if routine else None,  # ✅ `None` 체크 추가
        "special_routine_id": special_routine.id if special_routine else None  # ✅ `None` 체크 추가
    }

    return render(request, "myapp/routine.html", lists)

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
            return redirect('myapp/index.html')
        else:
            print("❌ 로그인 실패: 인증 실패")
            return render(request, 'commons/login.html', {'error': '아이디 또는 비밀번호가 틀렸습니다.'})
    
    return render(request, 'commons/login.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('myapp/index.html')
    else:
        form = UserForm()
    return render(request, 'commons/signup.html', {'form': form})


WEEKDAYS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}
@login_required
def get_routine_events(request):
    """ 사용자의 편지 루틴을 JSON 데이터로 반환 """
    user = request.user
    routines = LetterRoutine.objects.filter(user=user)
    special_dates = SpecialDateRoutine.objects.filter(user=user)

    today = datetime.today().date()
    events = []

    # 루틴 처리
    for routine in routines:
        # 주간 루틴
        if routine.routine_type == "weekly":
            weekday = routine.day_of_week
            if weekday:
                weekday_num = WEEKDAYS[weekday]
                next_date = today + timedelta(days=(weekday_num - today.weekday() + 7) % 7)
                for i in range(52):
                    events.append({
                        "id": routine.id,
                        "title": routine.title,
                        "start": (next_date + timedelta(weeks=i)).strftime("%Y-%m-%d"),
                        "allDay": True
                    }) 

        # 월간 루틴
        elif routine.routine_type == "monthly":
            for month in range(1, 13):
                try:
                    events.append({
                        "id": routine.id,
                        "title": routine.title,
                        "start": f"2025-{month:02d}-{routine.day_of_month:02d}",
                        "allDay": True
                    })
                except:
                    continue

    # 🎉 기념일(SpecialDateRoutine) 처리
    for special in special_dates:
        events.append({
            "title": f"🎉 {special.name}",
            "start": special.date.strftime("%Y-%m-%d"),
            "allDay": True,
            "color": "#3399ff"
        })

    return JsonResponse(events, safe=False)

def delete_routine(request, pk):
    try:
        routine = get_object_or_404(LetterRoutine, pk=pk, user=request.user)
        routine.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

