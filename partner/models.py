from django.db import models

from catalogue.models import Product


class Partner(models.Model):
    name = models.CharField(max_length=48)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class PartnerStock(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="partners")
    price = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.partner}------>{self.product}-----:{self.price}"
