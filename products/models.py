from django.db import models


class SiteSettings(models.Model):
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=80)

    def __str__(self):
        return "Site Settings"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    is_delivered = models.BooleanField(
        default=False,
        verbose_name="Done Delivered"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.name}"
