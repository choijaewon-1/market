import random
from django.core.mail import send_mail
from .models import VerificationCode


def send_verification_code(email):
    code = str(random.randint(100000, 999999))  # 6자리 난수
    VerificationCode.objects.create(email=email, code=code)

    subject = "[청주대학교 중고거래] 이메일 인증 코드"
    message = f"아래 인증 코드를 입력해 주세요:\n\n{code}"

    send_mail(subject, message, None, [email])
