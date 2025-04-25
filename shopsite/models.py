# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# 사용자 모델 (회원가입/로그인/마이페이지)
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)
    introduction = models.TextField(blank=True, null=True)
    is_suspended = models.BooleanField(default=False)  # 휴면/정지 여부
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)  # 잔액

    def __str__(self):
        return self.username

# 상품 모델
class Product(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# 채팅 메시지 (1:1 or 전체 채팅)
class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)  # 전체 채팅이면 True

    def __str__(self):
        return f"{self.sender.nickname} → {self.receiver.nickname if self.receiver else '전체'}: {self.message[:20]}"

# 신고 기능 (유저 또는 상품 대상)
class Report(models.Model):
    REPORT_TYPE = (
        ('USER', 'User'),
        ('PRODUCT', 'Product'),
    )
    reporter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_users', null=True, blank=True)
    reported_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.nickname} → {self.report_type}"

# 송금 기능
class Transaction(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    memo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.sender.nickname} → {self.receiver.nickname} : {self.amount}원"


# 상품 검색 로그 (선택적 기능)
class SearchLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    keyword = models.CharField(max_length=100)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname if self.user else '비회원'} 검색: {self.keyword}"
