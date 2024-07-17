from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, FormView

from shipping.forms import ShippingAddressForm
from shipping.models import ShippingAddress


@login_required
def address_list(request):
    addresses = ShippingAddress.objects.filter(user=request.user).order_by("-id")
    return render(
        request,
        "shipping/list.html",
        {"addresses": addresses},
    )


# class AddressListView(View):
#
#     @method_decorator(login_required)
#     def get(self, request):
#         addresses = ShippingAddress.objects.filter(user=request.user).order_by("-id")
#         return render(
#             request,
#             "shipping/list.html",
#             {"addresses": addresses},
#         )

# class AddressListView(TemplateView):
#     template_name = "shipping/list.html"
#
#     # @method_decorator(login_required)
#     # def get(self, request, *args, **kwargs):
#     #     context = self.get_context_data(**kwargs)
#     #     context["addresses"] = ShippingAddress.objects.filter(user=request.user).order_by("-id")
#     #     return  self.render_to_response(context)
#
#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["addresses"] = ShippingAddress.objects.filter(user=self.request.user).order_by("-id")
#         return context


class AddressListView(ListView):
    model = ShippingAddress
    template_name = "shipping/list.html"
    context_object_name = "addresses"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user).order_by("-id")
        return qs


@login_required
@require_http_methods(request_method_list=['GET', 'POST'])
def address_create(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("address_list")
    else:
        form = ShippingAddressForm()

    return render(
        request,
        "shipping/create.html",
        {"form": form}
    )


class AddressCreateView(FormView):
    template_name = "shipping/create.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("address_list")

    @method_decorator(login_required)
    @method_decorator(require_http_methods(request_method_list=['GET', 'POST']))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
