from django.contrib import admin
from django.contrib.admin import register

from partner.models import Partner, PartnerStock


@register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@register(PartnerStock)
class PartnerStockAdmin(admin.ModelAdmin):
    list_display = ["partner", "product", "price"]
    search_fields = ["partner__name"]