# diagnosis/serializers.py

from rest_framework import serializers
from .models import Disease, Symptom, SymptomReport, DiagnosisReport
from account.serializers import UserSerializer

# 1. 질병 시리얼라이저
class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'

# 2. 증상 시리얼라이저
class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

# 3. 증상 리포트 시리얼라이저 (Input 데이터 상세)
class SymptomReportSerializer(serializers.ModelSerializer):
    symptoms = SymptomSerializer(many=True, read_only=True)
    
    class Meta:
        model = SymptomReport
        fields = ['id', 'symptoms', 'user_description', 'created_at']

# 4. 진단 리포트 시리얼라이저 (최종 결과)
class DiagnosisReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    disease = DiseaseSerializer(read_only=True)
    symptom_report = SymptomReportSerializer(read_only=True)
    disease_id = serializers.PrimaryKeyRelatedField(
        queryset=Disease.objects.all(), source='disease', write_only=True
    )
    symptom_report_id = serializers.PrimaryKeyRelatedField(
        queryset=SymptomReport.objects.all(), source='symptom_report', write_only=True
    )

    class Meta:
        model = DiagnosisReport
        fields = [
            'id', 'user', 'disease', 'symptom_report', 
            'disease_id', 'symptom_report_id', # 입력용 필드
            'accuracy', 'diag_date'
        ]
        read_only_fields = ['diag_date']