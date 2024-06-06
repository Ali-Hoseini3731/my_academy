from django.urls import path
from transaction.views import transaction_list

urlpatterns = [
    path("list/", transaction_list, name="transaction_list"),
]