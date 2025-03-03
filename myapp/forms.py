from django import forms
from .models import Letters

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letters
        fields = ['title', 'content', 'image','category','open_date']  # 사용자 입력 필드

        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),  # 날짜 입력 필드
           
        }
