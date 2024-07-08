from django.urls import path

from shipping.views import list_address, create_address

urlpatterns = [
    path("list/", list_address, name="list_address"),
    path("create", create_address, name="create_address"),
]
