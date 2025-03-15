from django import forms
from .models import Letters, LetterRoutine
from .models import SpecialDateRoutine

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letters
        fields = ['title','mood', 'content', 'image','category','open_date']  # 사용자 입력 필드

        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control', 'style':'width: 350px; height:440px'}),
            'open_date': forms.DateInput(attrs={'type': 'date'}),  # 날짜 입력 필드
            
        }


class LetterRoutineForm(forms.ModelForm):
    class Meta:
        model = LetterRoutine
        fields = ['title', 'routine_type', 'day_of_week', 'day_of_month', 'time']

class SpecialDateRoutineForm(forms.ModelForm):
    class Meta:
        model = SpecialDateRoutine  # ✅ 올바른 모델 참조
        fields = ["name", "date"]  # ✅ 필요한 필드만 포함 (user 제거)