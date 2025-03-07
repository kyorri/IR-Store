from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    specification = models.FileField(upload_to="specifications/")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, default="images/missing_image.jpg"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")

    def __str__(self):
        return f"Cart of {self.user.username}"

    class Meta:
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return (
            f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
        )

    class Meta:
        verbose_name_plural = "Cart Items"
