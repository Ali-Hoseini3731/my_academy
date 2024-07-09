from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


@login_required
def list_address(request):
    addresses = ShippingAddress.objects.filter(user=request.user).order_by("-id")
    return render(
        request,
        'shipping/list.html',
        {"addresses": addresses}
    )


class ListAddressView(View):

    @method_decorator(login_required)
    def get(self, request):
        addresses = ShippingAddress.objects.filter(user=request.user).order_by("-id")
        return render(
            request,
            'shipping/list.html',
            {"addresses": addresses}
        )


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def create_address(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("list_address")

    else:
        form = ShippingAddressForm()
    return render(request, "shipping/create.html", {"form": form})
