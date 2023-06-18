from django.contrib import admin

from .models import Audio


class AudioAdmin(admin.ModelAdmin):
    list_display = ["title", "creator", "created_at"]
    list_filter = ["creator"]


admin.site.register(Audio, AudioAdmin)
