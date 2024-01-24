from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url=reverse_lazy("products:product_list"))),
    path("products/", include("demo.products.urls", namespace="products")),
]
