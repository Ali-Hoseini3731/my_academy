from django.db import models


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related("category", "brand", "product_type")

    def active(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).filter(is_active=True)

    def deactive(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs).exclude(is_active=True)


class ProductType(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=32)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("category_detail", args=[self.pk])


class Brand(models.Model):
    title = models.CharField(max_length=32)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="children", blank=True, null=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    INTEGER = 1
    FLOAT = 2
    STRING = 3
    ATTRIBUTE_TYPE_FIELDS = (
        (INTEGER, "Integer"),
        (FLOAT, "Float"),
        (STRING, "String",)
    )

    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="attributes")
    title = models.CharField(max_length=32)
    attribute_type = models.PositiveSmallIntegerField(choices=ATTRIBUTE_TYPE_FIELDS, default=INTEGER)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=32)
    upc = models.PositiveIntegerField(unique=True)
    description = models.TextField(blank=True, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}--{self.upc}--{self.description}--{self.product_type}--{self.category}"

    @property
    def stock(self):
        return self.partners.all().order_by('price').first()

    @property
    def stocks(self):
        return self.partners.all().order_by("price")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("product_detail", args=[self.pk])

    default_manager = models.Manager()
    objects = ProductManager()


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return str(self.product)


class ProductAttributeValue(models.Model):
    value = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="values")
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name="values")

    def __str__(self):
        return f"{self.product} <{self.product_attribute}> : {self.value}"
