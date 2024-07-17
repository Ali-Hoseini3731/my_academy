from django.urls import path
from catalogue.views import (products_list, product_detail, category_detail,
                             brand_products, product_search, ProductsListView, ProductDetailView)

urlpatterns = [
    # path("products/list/", products_list, name="products_list"),
    path("products/list/", ProductsListView.as_view(), name="products_list"),
    # path("product/detail/<int:pk>/", product_detail, name="product_detail"),
    path("product/detail/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/search/", product_search, name="product_search"),
    path("category/<int:pk>/products/", category_detail, name="category_detail"),
    path("brand/<int:pk>/products/", brand_products, name="brand_products"),
]
