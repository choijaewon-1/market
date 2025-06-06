from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# ✅ 1단계 이메일 입력 폼
class EmailForm(forms.Form):
    email = forms.EmailField(label="학교 이메일")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith("@cju.ac.kr"):
            raise ValidationError("청주대학교 이메일(@cju.ac.kr)만 허용됩니다.")
        return email

# ✅ 2단계 인증코드 입력 폼
class CodeForm(forms.Form):
    code = forms.CharField(label="인증 코드", max_length=6)

# ✅ 3단계 최종 사용자 정보 입력 폼
class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")
