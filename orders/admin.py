from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    Industry-style readable, safe, and scalable.
    """

    # ==================================================
    # LIST PAGE (Table View)
    # ==================================================

    list_display = (
        "id",
        "user",
        "status",
        "total_amount",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "id",
        "user__username",
        "user__email",
    )

    ordering = ("-created_at",)

    list_per_page = 25

    # ==================================================
    # DETAIL / EDIT PAGE
    # ==================================================

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Order Details", {
            "fields": ("id", "user", "status", "total_amount")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at")
        }),
    )

    # ==================================================
    # USABILITY
    # ==================================================

    autocomplete_fields = ("user",)

    # ==================================================
    # CUSTOM ACTIONS
    # ==================================================

    actions = ["mark_as_cancelled"]

    @admin.action(description="Mark selected orders as CANCELLED")
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status=Order.Status.CANCELLED)
