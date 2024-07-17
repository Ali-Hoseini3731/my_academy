from django.contrib.auth.decorators import login_required
from django.urls import path
from shipping.views import address_list, address_create, AddressListView, AddressCreateView

urlpatterns = [
    # path("list/", address_list, name="address_list"),
    # path("list/", login_required(AddressListView.as_view()), name="address_list"),
    path("list/", AddressListView.as_view(), name="address_list"),
    # path("create/", address_create, name="address_create"),
     path("create/", AddressCreateView.as_view(), name="address_create"),
]
