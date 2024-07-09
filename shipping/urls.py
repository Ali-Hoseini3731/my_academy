from django.urls import path

from shipping.views import create_address, ListAddressView

urlpatterns = [
    path("list/", ListAddressView.as_view(), name="list_address"),
    path("create", create_address, name="create_address"),
]
