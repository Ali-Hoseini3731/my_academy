from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


class ListAddressView(ListView):
    model = ShippingAddress
    template_name = "shipping/list.html"
    context_object_name = "addresses"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)



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
