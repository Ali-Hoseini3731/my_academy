from django.contrib import admin
from django.contrib.admin import register

from catalogue.models import Category, Brand, ProductType, ProductAttribute, Product, ProductImage


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "created_time"]
    inlines = [ProductAttributeInline]


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["title", "product_type", "attribute_type"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["upc", "title", "product_type", "category", "brand", "description", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]
    list_display_links = ["title", "upc"]
    search_fields = ["title", "upc", "category__title", "brand__title"]
    inlines = [ProductImageInline]


@register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["image", "product"]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
