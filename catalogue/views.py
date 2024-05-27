from django.db.models import Q
from django.http import HttpResponse

from catalogue.models import Product


def products_list(request):
    products = Product.objects.select_related("category").all()
    context = [
        (f"{product.title}--{product.upc}--{product.product_type}"
         f"--{product.category.title}--{product.brand}--{product.is_active} <br>") for product in products
    ]
    return HttpResponse(context)


def product_detail(request, pk):
    try:
        product = Product.objects.get(Q(pk=pk) | Q(upc=pk))
    except Product.DoesNotExist:
        return HttpResponse("this product does not exist")

    return HttpResponse(product)


def category_products(request, pk):
    pass
