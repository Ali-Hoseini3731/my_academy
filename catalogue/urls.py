from django.urls import path
from catalogue.views import products_list, product_detail, category_products

urlpatterns = [
    path("products/list/", products_list, name="products_list"),
    path("product/detail/<int:pk>/", product_detail, name="product_detail"),
    path("category/<int:pk>/products/", category_products, name="category_products"),
]