from django.db import models
from . import managers


class TimeStampModel(models.Model):
    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = managers.CustomModelManager()

    # "abstract = True" Makes this models not to be installed in DB
    # For extend other apps models
    class Meta:
        abstract = True
