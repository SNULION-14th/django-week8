from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  """
  공통 계정
  - username, password만 사용
  - name, phone, role 추가
  """
  name = models.CharField(max_length=10) # 실명
  phone = models.CharField(max_length=15, blank=True)
  role = models.CharField(max_length=10) # "TEACHER", "STUDENT", "PARENT"

  def __str__(self):
    return f"{self.username}: {self.role}"
  
class Teacher(models.Model):
  user = models.OneToOneField(
    to='User', 
    on_delete=models.CASCADE, 
    related_name='teacher'
  )

  major = models.CharField(max_length=100, blank=True)
  bio = models.CharField(max_length=100, blank=True) # 한 줄 소개
  career = models.TextField(blank=True)

  def __str__(self):
    return f"{self.user.name} 선생님"

class Parent(models.Model):
  user = models.OneToOneField(
    to='User', 
    on_delete=models.CASCADE, 
    related_name='parent'
  )

  relationship = models.CharField(max_length=50) # 학생과의 관계
  memo = models.TextField(blank=True) # 기타 특이 사항 등

  def __str__(self):
      return f"{self.user.name} 학부모님"

class Student(models.Model):
  user = models.OneToOneField(
    to='User',
    on_delete=models.CASCADE,
    related_name='student'
  )

  parent = models.ForeignKey(
    to='Parent',
    on_delete=models.SET_NULL, # 학부모 삭제해도 학생 정보 유지
    null=True,
    blank=True,
    related_name='students'
  )

  age = models.PositiveIntegerField()
  school = models.CharField(max_length=100, blank=True)
  goal = models.TextField(blank=True)

  def __str__(self):
      return f"{self.user.name} 학생"  