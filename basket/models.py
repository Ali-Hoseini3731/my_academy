from django.contrib.auth.models import User
from django.db import models

from catalogue.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="baskets", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    @classmethod
    def get_basket(cls, basket_id):
        if basket_id is None:
            basket = cls.objects.create()
        else:
            try:
                basket = cls.objects.get(id=basket_id)
            except cls.DoesNotExist:
                basket = None
        return basket

    def validate_user(self, user):
        if user.is_authenticated:
            if self.user is not None and self.user != user:
                return False
            if self.user is None:
                self.user = user
                self.save()
        elif user is not None:
            return False

        return True

    def add(self, product, quantity=1):
        if self.lines.filter(product=product).exists():
            product_line = self.lines.get(product=product)
            product_line.quantity += quantity
            product_line.save()
        else:
            product_line = self.lines.create(product=product, quantity=quantity)

        return product_line


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="lines")
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.basket} =====> {self.product} --- {self.quantity}"
