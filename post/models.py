# ./post/models.py
from django.db import models
from django.conf import settings # 커스텀 User 모델을 참조하기 위해 가져옵니다.

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    edition = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} ({self.edition})"

class Post(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', '대여 가능'),
        ('RESERVED', '예약 중'),
        ('RENTED', '대여 중'),
    ]
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    condition = models.TextField()
    deposit = models.PositiveIntegerField(help_text="보증금")
    rental_fee = models.PositiveIntegerField(help_text="대여료")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return self.title

# (이하 Comment, Transaction, Review 모델도 동일하게 settings.AUTH_USER_MODEL을 사용하여 추가해 줍니다.)