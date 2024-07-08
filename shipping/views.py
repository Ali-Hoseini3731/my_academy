from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from shipping.forms import ShippingAddressForm


def list_address(request):
    return HttpResponse("address list")


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
