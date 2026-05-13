from django.db import models
from datetime import date
from django.conf import settings

class ClassInfo(models.Model):
  """
  수업에 대한 정보.
  선생님, 학생, 학부모 연결
  """

  # 담당 선생님
  teacher = models.ForeignKey(
    to='account.Teacher',
    on_delete=models.CASCADE,
    related_name='classes'
  )

  # 수강 학생
  student = models.ForeignKey(
    to='account.Student',
    on_delete=models.CASCADE,
    related_name='classes'
  )
  
  # 수강 학생의 학부모
  parent = models.ForeignKey(
    to='account.Parent',
    on_delete=models.CASCADE,
    related_name='classes'
  )
  
  # 수업 과목
  subject = models.CharField(max_length=256)

  def __str__(self):
      return f"{self.student.user.name} 학생: [{self.subject}] 수업"
  

class ClassLog(models.Model):
  """
  수업 일지. 진도 내용 및 숙제 기록
  """

  # 연결된 수업
  class_info = models.ForeignKey(
    to='ClassInfo', 
    on_delete=models.CASCADE,
    related_name='logs'
  )

  date = models.DateField(default=date.today)
  content = models.TextField()

  # 숙제 없는 날 대비 blank 허용
  hw = models.TextField(blank=True)

  def __str__(self):
      return (
        f"{self.date.strftime('%Y-%m-%d')} "
        f"[{self.class_info.student.user.name}] "
        f"[{self.class_info.subject}] 수업 일지"
      )
  