from django.db import models
from django.conf import settings

# 1. 질병 모델 (Disease)
class Disease(models.Model):
    name = models.CharField(max_length=100) # 병명

    def __str__(self):
        return self.name

# 2. 증상 모델 (Symptom)
class Symptom(models.Model):
    name = models.CharField(max_length=100) # 증상명

    def __str__(self):
        return self.name

# 3. 진단 리포트 (DiagnosisReport)
class SymptomReport(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    # 사용자가 선택한 여러 증상들
    symptoms = models.ManyToManyField(Symptom)
    # 직접 입력하는 상세 내용
    user_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}의 증상 리포트 ({self.created_at.date()})"

class DiagnosisReport(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    
    symptom_report = models.ForeignKey(
        SymptomReport, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='diagnoses'
    )
    
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    accuracy = models.IntegerField()
    diag_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease.name} 진단 결과"