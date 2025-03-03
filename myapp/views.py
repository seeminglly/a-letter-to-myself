from django.shortcuts import render, redirect
from .models import Letters
from .forms import LetterForm
from django.utils.timezone import now  # 현재 날짜 가져오기
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


# 2️⃣ 작성된 편지 목록 보기
def letter_list(request):
    letters = Letters.objects.all().order_by('-created_at')  # 최신 순 정렬
    print("🔵 가져온 편지 개수:", letters.count())  # 콘솔에 출력
    print("🔵 가져온 편지 목록:", list(letters.values()))  # 데이터 출력
    return render(request, 'myapp/letter_list.html', {'letters': letters})


    