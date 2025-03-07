from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import Letters, LetterRoutine
from .forms import LetterForm
from django.utils.timezone import now  # 현재 날짜 가져오기
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'myapp/index.html')

# 1️⃣ 편지 작성 뷰
def write_letter(request):
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():
            letter = form.save(commit=False)
            if not letter.open_date:  # open_date가 없으면 오늘 날짜로 설정
                letter.open_date = now().date()
            letter.save()
            return redirect('letter_list')  # 편지 목록 페이지로 이동
    else:
        form = LetterForm()
        
    return render(request, 'myapp/writing.html', {'form': form})

def postbox(request):
    return render(request, 'myapp/postbox.html')

# 2️⃣ 작성된 편지 목록 보기
def letter_list(request):
    letters = Letters.objects.all()
    for letter in letters:
        print(f"Letter ID: {letter.id}")
    return render(request, 'myapp/letter_list.html', {'letters':letters})

def past_letters(request):
    """ 과거의 편지 목록 (오늘 이전 날짜) """
    today = now().date()
    letters = Letters.objects.filter(open_date__lt=today)
    return render(request, 'myapp/letter_past.html', {'letters': letters})

def today_letters(request):
    """ 오늘의 편지 목록 """
    today = now().date()  # 오늘 날짜 가져오기
    letters = Letters.objects.filter(open_date=today)
    
    print(f"오늘 날짜: {today}")
    print(f"오늘의 편지 개수: {letters.count()}")

    for letter in letters:
        print(f"Letter ID: {letter.id}, Title: {letter.title}, Open Date: {letter.open_date}")

    return render(request, 'myapp/letter_today.html', {'letters': letters})


def future_letters(request):
    """ 미래의 편지 목록 (오늘 이후 날짜) """
    today = now().date()
    letters = Letters.objects.filter(open_date__gt=today)
    return render(request, 'myapp/letter_future.html', {'letters': letters})

#개별 편지 상세보기api
def letter_json(request, letter_id):
    letter = get_object_or_404(Letters, id=letter_id)
    data = {
        'id':letter.id,
        'title': letter.title,
        'content': letter.content,
        'letter_date': letter.open_date.strftime("%Y-%m-%d"),
    }
    return JsonResponse(data)

#편지 루틴 만들기
@login_required
def save_routine(request):
    days = range(1, 32) 
    if request.method == "POST":
        routine_type = request.POST.get("routine_type")
        day_of_week = request.POST.get("day_of_week") if routine_type == "weekly" else None
        day_of_month = request.POST.get("day_of_month") if routine_type == "monthly" else None
        time = request.POST.get("time")

        LetterRoutine.objects.create(
            user=request.user,
            routine_type=routine_type,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            time=time
        )
        return redirect("home")

    return render(request, "myapp/routine.html",  {'days': days})

   

 