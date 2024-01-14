from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def slug(self):
        return self.name.lower().replace(" ", "-")
