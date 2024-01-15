# IMPORTS:START
from demo.core.utils import paginate_queryset
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .forms import ProductForm
from .models import Product

# IMPORTS:END


# CODE:START
def product_list(request: HttpRequest):
    products = Product.objects.all()
    template_name = "products/product_list.html#table" if request.htmx else "products/product_list.html"  # type: ignore
    return TemplateResponse(
        request,
        template_name,
        context={"products_page": paginate_queryset(request, products)},
    )


def product_detail(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    return TemplateResponse(
        request,
        "products/product_detail.html",
        context={"product": product},
    )


def product_create(request: HttpRequest):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:product_list")
    return TemplateResponse(
        request,
        "products/product_create.html",
        context={"form": form},
    )


def product_update(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:product_detail", pk=pk)
    return TemplateResponse(
        request,
        "products/product_update.html",
        context={"product": product, "form": form},
    )


@require_http_methods(["DELETE"])
def product_delete(_: HttpRequest, pk: int):
    Product.objects.filter(pk=pk).delete()
    return HttpResponse("")


# CODE:END
