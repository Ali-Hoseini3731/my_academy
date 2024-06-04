from django.db.models import Q
from django.http import HttpResponse

from catalogue.models import Product, Category, Brand


def products_list(request):
    products = Product.objects.select_related("category", "brand", "product_type").all()
    context = [
        (f"{product.title}--{product.upc}--{product.product_type.title}"
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
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)

    except Category.DoesNotExist:
        return HttpResponse("category does not exist")

    products = category.products.all()
    return HttpResponse(
        [f"{product.title}--{product.upc}--{product.category.title} <br>" for product in products]
    )


def brand_products(request, pk):
    try:
        brand = Brand.objects.prefetch_related("products").get(pk=pk)
    except Brand.DoesNotExist:
        return HttpResponse("this brand does not exist")

    products = brand.products.all()
    context = [f"{product.title}--{product.upc}--{product.brand}<br>" for product in products]
    return HttpResponse(context)
