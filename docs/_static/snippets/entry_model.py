from django.contrib.auth.models import User
from django.db import models
from falco_toolbox.models import TimeStamped


class Entry(TimeStamped):
    # the TimeStampedModel adds the fields `created` and `modified` so we don't need to add them
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")

    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"
