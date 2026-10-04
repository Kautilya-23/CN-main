from django.contrib import admin
from .models import Hospital, LabReportHistory

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'facility_category', 'hospital_type', 'rating')
    list_filter = ('facility_category', 'hospital_type', 'city')
    search_fields = ('name', 'city', 'address')

admin.site.register(LabReportHistory)
