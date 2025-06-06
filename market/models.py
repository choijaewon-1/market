from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('도서', '도서'),
        ('전자기기', '전자기기'),
        ('생활용품', '생활용품'),
        ('기타', '기타'),
    ]

    STATUS_CHOICES = [
        ('판매 중', '판매 중'),
        ('예약 중', '예약 중'),
        ('판매 완료', '판매 완료'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.PositiveIntegerField()  # 💰 가격 추가
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='기타')  # 📂 카테고리
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='판매 중')    # 🔄 거래 상태

    def __str__(self):
        return self.title
