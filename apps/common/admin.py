from django.contrib import admin

from .models import PaymentPlan


class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = ["content", "type", "price"]
    list_filter = ["content"]


admin.site.register(PaymentPlan, PaymentPlanAdmin)
