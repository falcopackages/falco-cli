# IMPORTS:START
from django.forms import ModelForm

from .models import Product

# IMPORTS:END


# CODE:START
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "price", "sku", "created_at")


# CODE:END
