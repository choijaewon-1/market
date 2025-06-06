from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import EmailForm, CodeForm, StudentSignUpForm
from .models import VerificationCode
from .utils import send_verification_code
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# 1단계: 이메일 입력 및 인증 코드 전송
def signup_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            send_verification_code(email)
            request.session['signup_email'] = email
            return redirect('signup_verify')
    else:
        form = EmailForm()
    return render(request, 'accounts/signup_email.html', {'form': form})

# 2단계: 인증 코드 입력 및 검증
def signup_verify(request):
    email = request.session.get('signup_email')
    if not email:
        return redirect('signup_email')

    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code_input = form.cleaned_data['code']
            try:
                code_obj = VerificationCode.objects.filter(email=email, code=code_input).latest('created_at')
                if code_obj.is_expired():
                    form.add_error(None, "인증 코드가 만료되었습니다.")
                else:
                    request.session['verified_email'] = email
                    return redirect('signup_complete')
            except VerificationCode.DoesNotExist:
                form.add_error(None, "인증 코드가 유효하지 않습니다.")
    else:
        form = CodeForm()
    return render(request, 'accounts/signup_verify.html', {'form': form})

# 3단계: 최종 회원가입 정보 입력
def signup_complete(request):
    email = request.session.get('verified_email')
    if not email:
        return redirect('signup_email')

    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.save()
            login(request, user)
            return redirect('home')  # 가입 후 이동할 페이지
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup_complete.html', {'form': form})

# 로그인
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('home')
