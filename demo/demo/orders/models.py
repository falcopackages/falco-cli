from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    products = models.ManyToManyField("products.Product")
    created = models.DateTimeField(auto_now_add=True)
