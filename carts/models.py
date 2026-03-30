import uuid

from django.conf import settings
from django.db import models
from store.models import Product

class Cart(models.Model):
    # هر کاربر فقط یک سبد خرید فعال دارد
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سبد خرید {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        # جلوگیری از تکرار یک محصول در یک سبد خرید
        unique_together = [['cart', 'product']]
