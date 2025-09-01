from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Assignment, Submission


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "is_teacher", "is_student", "is_staff")
    list_filter = ("is_teacher", "is_student", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Roles", {"fields": ("is_teacher", "is_student")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    
    
admin.site.register(Assignment)
admin.site.register(Submission)