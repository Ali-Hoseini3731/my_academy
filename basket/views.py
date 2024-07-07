from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST

from basket.forms import AddToBasketForm
from basket.models import Basket
from catalogue.models import Product


@require_POST
def add_to_basket(request):
    response = HttpResponseRedirect(request.POST.get("next", "/catalogue/products/list/"))
    basket = Basket.get_basket(request.COOKIES.get("basket_id", None))

    if basket is None:
        return HttpResponse("this basket does not exist")
    response.set_cookie("basket_id", basket.id)

    if not basket.validate_user(request.user):
        return HttpResponse("invalid user")

    form = AddToBasketForm(request.POST)
    if form.is_valid():
        form.save(basket)

    return response
