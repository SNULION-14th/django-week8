# diagnosis/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .models import DiagnosisReport, Disease, SymptomReport
from .serializers import DiagnosisReportSerializer

class DiagnosisListView(APIView):
    @extend_schema(
        summary="진단 리포트 목록 조회",
        description="로그인한 유저의 모든 진단 기록을 가져옵니다.",
        responses={200: DiagnosisReportSerializer(many=True)}
    )
    def get(self, request):
        # 💡 최적화: select_related와 prefetch_related로 한 번에 다 가져옵니다.
        reports = DiagnosisReport.objects.filter(user=request.user).select_related(
            'user', 'disease', 'symptom_report'
        ).prefetch_related('symptom_report__symptoms')
        
        serializer = DiagnosisReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="진단 리포트 생성",
        description="증상 리포트 ID를 받아 새로운 진단 기록을 만듭니다.",
        request=DiagnosisReportSerializer,
        responses={201: DiagnosisReportSerializer}
    )
    def post(self, request):
        # 💡 수정된 로직: 이제 symptom_report_id를 함께 받아야 합니다.
        symptom_report_id = request.data.get('symptom_report_id')
        disease_id = request.data.get('disease_id')
        accuracy = request.data.get('accuracy', 0)

        symptom_report = get_object_or_404(SymptomReport, id=symptom_report_id)
        disease = get_object_or_404(Disease, id=disease_id)

        # 수동으로 객체를 생성하거나 시리얼라이저에 넘겨줍니다.
        diagnosis = DiagnosisReport.objects.create(
            user=request.user,
            symptom_report=symptom_report,
            disease=disease,
            accuracy=accuracy
        )
        
        serializer = DiagnosisReportSerializer(diagnosis)
        return Response(serializer.data, status=status.HTTP_201_CREATED)