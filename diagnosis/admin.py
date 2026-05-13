# diagnosis/admin.py

from django.contrib import admin
from .models import Disease, Symptom, SymptomReport, DiagnosisReport

admin.site.register(Disease)
admin.site.register(Symptom)

@admin.register(SymptomReport)
class SymptomReportAdmin(admin.ModelAdmin):
    filter_horizontal = ('symptoms',) 
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)

@admin.register(DiagnosisReport)
class DiagnosisReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'disease', 'accuracy', 'diag_date')
    list_filter = ('disease',)