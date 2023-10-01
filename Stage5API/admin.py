from django.contrib import admin
from .models import Stream
# Register your models here.

@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ("__str__", "started_at", "is_live")
    readonly_fields = ("hls_url",)