from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carts.models import Cart, CartItem
from store.models import Category, Product

from .models import Order, OrderItem

User = get_user_model()


def _category(**kwargs):
    defaults = {'title': 'Cat', 'slug': 'cat'}
    defaults.update(kwargs)
    return Category.objects.create(**defaults)


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


class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='u@example.com', password='x')

    def test_default_payment_status_pending(self):
        order = Order.objects.create(user=self.user)
        self.assertEqual(order.payment_status, Order.PAYMENT_STATUS_PENDING)

    def test_cannot_delete_user_with_orders(self):
        Order.objects.create(user=self.user)
        with self.assertRaises(ProtectedError):
            self.user.delete()


class OrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='buyer@example.com', password='secret')
        self.other = User.objects.create_user(email='other@example.com', password='secret')
        self.category = _category(slug='tech')
        self.product = _product(self.category, name='Book', slug='book', inventory=5)

    def _auth(self, user=None):
        self.client.force_authenticate(user=user or self.user)

    def _seed_cart(self, user, quantity=2):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=quantity)

    def test_create_order_from_cart_returns_201(self):
        self._auth()
        self._seed_cart(self.user)

        response = self.client.post(reverse('orders-list'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.unit_price, self.product.price)

    def test_create_order_clears_cart_and_reduces_inventory(self):
        self._auth()
        self._seed_cart(self.user, quantity=2)
        before = self.product.inventory

        self.client.post(reverse('orders-list'), {}, format='json')

        self.product.refresh_from_db()
        self.assertEqual(self.product.inventory, before - 2)
        self.assertFalse(
            CartItem.objects.filter(cart__user=self.user).exists()
        )

    def test_create_order_without_cart_returns_400(self):
        self._auth()

        response = self.client.post(reverse('orders-list'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_empty_cart_returns_400(self):
        self._auth()
        Cart.objects.create(user=self.user)

        response = self.client.post(reverse('orders-list'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_insufficient_inventory_returns_400(self):
        self._auth()
        self._seed_cart(self.user, quantity=100)

        response = self.client.post(reverse('orders-list'), {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_only_returns_own(self):
        self._seed_cart(self.user, quantity=1)
        self._seed_cart(self.other, quantity=1)
        self._auth(self.user)
        self.client.post(reverse('orders-list'), {}, format='json')
        self._auth(self.other)
        self.client.post(reverse('orders-list'), {}, format='json')

        self._auth(self.user)
        response = self.client.get(reverse('orders-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], Order.objects.get(user=self.user).id)

    def test_retrieve_other_users_order_returns_404(self):
        self._seed_cart(self.other, quantity=1)
        self.client.force_authenticate(self.other)
        self.client.post(reverse('orders-list'), {}, format='json')
        order_id = Order.objects.get(user=self.other).id

        self._auth(self.user)
        response = self.client.get(reverse('orders-detail', args=[order_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
