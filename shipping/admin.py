from django.contrib import admin
from django.contrib.admin import register

from shipping.models import ShippingAddress


@register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "zipcode", "number", "address", "created_time"]
    list_filter = ["user"]
