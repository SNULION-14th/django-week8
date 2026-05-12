from django.db import models

# Create your models here.
from django.utils import timezone

# 1. 학교 정보
class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)  
    tuition = models.IntegerField(verbose_name="등록금")
    region = models.CharField(max_length=100, verbose_name="지역")

    def __str__(self):
        return self.name

# 2. 장학금 정보
class Scholarship(models.Model):
    scholarship_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256, verbose_name="장학금 이름")
    amount = models.IntegerField(verbose_name="금액")
    benefit = models.TextField(verbose_name="혜택")
    provider = models.CharField(max_length=100, verbose_name="제공주체")
    deadline = models.DateTimeField(verbose_name="마감일")
    min_grade = models.FloatField(verbose_name="최소 학점")
    description = models.TextField(verbose_name="상세 설명")

    def __str__(self):
        return self.title

# 3. 유저 정보
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, verbose_name="이름")
    password = models.CharField(max_length=256, verbose_name="비밀번호")

    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="학교번호")
    income_range = models.IntegerField(verbose_name="소득분위")
    major_id = models.IntegerField(verbose_name="전공번호") 

    def __str__(self):
        return self.username

# 4. 전공분야 
class ScholarshipMajor(models.Model):
    major_id = models.IntegerField(verbose_name="전공번호")
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('major_id', 'scholarship'),)

# 5. 소득분위 
class ScholarshipIncome(models.Model):
    income_range = models.IntegerField(verbose_name="소득분위")
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('income_range', 'scholarship'),)

# 6. 지원한 장학금 목록 
class UserScholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, verbose_name="상태")
    saved_at = models.DateTimeField(default=timezone.now, verbose_name="저장시간")

    def __str__(self):
        return f"{self.user.username} - {self.scholarship.title}"