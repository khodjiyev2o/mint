from django.contrib import admin

from .models import Audio, UserContent, UserContentPaymentPlan


class AudioAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created_at"]
    list_filter = ["creator"]


admin.site.register(Audio, AudioAdmin)


class UserContentAdmin(admin.ModelAdmin):
    list_display = ["preventa_audio", "order", "created_at"]
    list_filter = ["user"]


admin.site.register(UserContent, UserContentAdmin)


class UserContentPaymentPlanAdmin(admin.ModelAdmin):
    list_display = ["content", "user", "created_at"]
    list_filter = ["user"]


admin.site.register(UserContentPaymentPlan, UserContentPaymentPlanAdmin)
