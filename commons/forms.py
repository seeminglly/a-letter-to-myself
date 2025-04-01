from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="필수 입력 항목입니다.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용 중인 이메일입니다.")
        return email
    
class ProfileForm(forms.ModelForm): # 프로필 수정 필드 추가
    password = None
    class Meta:
        model = Profile
        fields = ["nickname", "bio", "birthday", "blog_url"]

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]
