from django.contrib import admin

from .models import Category
from .models import Product

admin.site.register(Product)
admin.site.register(Category)
