from django.contrib import admin
from .models import Category, RepairHistory, RepairRequest, Technician


@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "phone", "email", "is_active")
    list_filter = ("is_active", "specialization")
    search_fields = ("name", "specialization", "email", "phone")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(RepairRequest)
class RepairRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "location", "priority", "status", "assigned_technician", "reporter", "created_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("location", "problem", "reporter__username")


@admin.register(RepairHistory)
class RepairHistoryAdmin(admin.ModelAdmin):
    list_display = ("repair_request", "old_status", "new_status", "technician", "changed_by", "created_at")
    list_filter = ("new_status", "created_at")
    search_fields = ("repair_request__id", "notes")
    readonly_fields = ("created_at",)
