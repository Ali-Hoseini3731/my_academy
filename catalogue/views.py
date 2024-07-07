from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render

from basket.forms import AddToBasketForm
from catalogue.models import Product, Category, Brand


def products_list(request):
    context = dict()
    context["products"] = Product.objects.all()
    context["categories"] = Category.objects.all()
    return render(request, "catalogue/product-list.html", context)


def product_detail(request, pk):
    # try:
    #     product = Product.objects.get(Q(pk=pk) | Q(upc=pk))
    # except Product.DoesNotExist:
    #     return HttpResponse("this product does not exist")

    queryset = Product.objects.filter(Q(pk=pk) | Q(upc=pk))
    if queryset.exists():
        product = queryset.first()
        form = AddToBasketForm({"product": product.id, "quantity": 1})
        return render(
            request,
            "catalogue/product_detail.html",
            {"product": product, "form": form}
        )
    return HttpResponse("product does not exist")


def product_search(request):
    title = request.GET.get("title")
    products = Product.objects.filter(is_active=True, title__icontains=title)
    context = [f"{product.title}--{product.upc}---{product.stock}<br>" for product in products]
    return HttpResponse(context)


def category_detail(request, pk):
    try:
        category = Category.objects.prefetch_related("products").get(pk=pk)

    except Category.DoesNotExist:
        return HttpResponse("category does not exist")

    products = category.products.all()
    return render(request, "catalogue/category_detail.html", {"products": products})


def brand_products(request, pk):
    try:
        brand = Brand.objects.prefetch_related("products").get(pk=pk)
    except Brand.DoesNotExist:
        return HttpResponse("this brand does not exist")

    products = brand.products.all()
    context = [f"{product.title}--{product.upc}--{product.brand}<br>" for product in products]
    return HttpResponse(context)
