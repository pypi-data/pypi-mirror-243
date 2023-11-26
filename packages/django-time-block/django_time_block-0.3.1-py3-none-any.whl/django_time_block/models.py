"""
models
"""

from django.db import models

# Create your models here.


class TimeBlock(models.Model):
    """
    a time block contains a duration [start_datetime: end_datetime) (not include the end_datetime)
    """
    object_id = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        indexes = [
                models.Index(fields=["object_id", "start_datetime"])
        ]
