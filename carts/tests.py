from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from store.models import Category, Product

from .models import Cart, CartItem

User = get_user_model()


def _product(category, **kwargs):
    defaults = {
        'name': 'Item',
        'description': 'Desc',
        'price': Decimal('10.00'),
        'inventory': 10,
        'category': category,
    }
    defaults.update(kwargs)
    return Product.objects.create(**defaults)


class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@example.com', password='x')
        self.category = Category.objects.create(title='Cat', slug='cat')

    def test_cart_one_to_one_per_user(self):
        Cart.objects.create(user=self.user)
        with self.assertRaises(IntegrityError):
            Cart.objects.create(user=self.user)

    def test_cart_str_includes_user_email(self):
        cart = Cart.objects.create(user=self.user)
        self.assertIn(self.user.email, str(cart))

    def test_deleting_user_removes_cart(self):
        cart = Cart.objects.create(user=self.user)
        pk = cart.pk
        self.user.delete()
        self.assertFalse(Cart.objects.filter(pk=pk).exists())


class CartItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@example.com', password='x')
        self.cart = Cart.objects.create(user=self.user)
        self.category = Category.objects.create(title='Cat', slug='cat')
        self.product = _product(self.category, name='P1', slug='p1')

    def test_unique_cart_product_pair(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_default_quantity(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product)
        self.assertEqual(item.quantity, 1)

    def test_deleting_cart_removes_items(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product)
        item_pk = item.pk
        self.cart.delete()
        self.assertFalse(CartItem.objects.filter(pk=item_pk).exists())
