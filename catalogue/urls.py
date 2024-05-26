from django.urls import path
from catalogue.views import products_list

urlpatterns = [
    path("products/list/", products_list, name="products_list")
]