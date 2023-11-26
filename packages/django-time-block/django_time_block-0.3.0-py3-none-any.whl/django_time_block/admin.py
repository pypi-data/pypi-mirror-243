"""
admin page for django block
"""


from django.contrib import admin

from .models import TimeBlock


@admin.register(TimeBlock)
class TimeBlockAdmin(admin.ModelAdmin):
    """
    TimeBlock Admin
    """
    list_display = ["object_id", "start_datetime", "end_datetime"]
