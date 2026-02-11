from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom User model.
    """

    # ==============================
    # LIST PAGE
    # ==============================

    list_display = (
        "email",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
    )

    ordering = ("-date_joined",)

    # ==============================
    # DETAIL PAGE
    # ==============================

    readonly_fields = (
        "id",
        "date_joined",
        "last_login",
    )

    fieldsets = (
        ("Account Info", {
            "fields": ("id", "email", "password")
        }),
        ("Permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_active", "is_staff"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")

