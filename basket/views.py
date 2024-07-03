from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

from basket.models import Basket
from catalogue.models import Product


@require_POST
def add_to_basket(request):
    response = HttpResponseRedirect(request.POST.get("next", "/catalogue/products/list/"))
    basket_id = request.COOKIES.get("basket_id", None)

    if basket_id is None:
        basket = Basket.objects.create()
        response.set_cookie("basket_id", basket.id)
    else:
        try:
            basket = Basket.objects.get(id=basket_id)
        except Basket.DoesNotExist:
            return HttpResponse("this basket dose not exist")

    if request.user.is_authenticated:
        if basket.user is not None and basket.user != request.user:
            return HttpResponse("this user does not have basket")
        basket.user = request.user
        basket.save()

    product_id = request.POST.get("product_id", None)
    quantity = int(request.POST.get("quantity", 1))
    if product_id is not None:
        try:
            product = Product.objects.get(id=product_id)
            basket.add_to_basket(product, quantity)
        except Product.DoesNotExist:
            return HttpResponse("this product does not exist")

    return response
