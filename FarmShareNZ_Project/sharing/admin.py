from django.contrib import admin
from .models import Equipment,RentalRequest,Report
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin): list_display=('name','category','owner','location','daily_rate','is_available'); list_filter=('category','is_available'); search_fields=('name','location','owner__username')
@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin): list_display=('equipment','requester','start_date','end_date','status'); list_filter=('status',)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin): list_display=('equipment','reporter','status','created_at'); list_filter=('status',)
