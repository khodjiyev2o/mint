from django.contrib import admin

from apps.payment.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_amount", "payment_type", "provider", "is_paid", "is_canceled")
    list_display_links = ("id", "user")
    list_filter = ("payment_type", "provider", "is_paid", "is_canceled")
    search_fields = ("id", "user__username", "user__email", "user__full_name", "total_amount", "audio__title")
