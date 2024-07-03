from django.contrib import admin
from django.contrib.admin import register

from basket.models import Basket, BasketLine


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    extra = 1


@register(BasketLine)
class BasketLineAdmin(admin.ModelAdmin):
    list_display = ["basket", "product", "quantity"]


class BasketAdmin(admin.ModelAdmin):
    list_display = ["user"]
    list_filter = ["user"]
    inline = [BasketLineInline]


admin.site.register(Basket, BasketAdmin)
