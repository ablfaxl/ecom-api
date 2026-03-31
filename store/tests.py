from decimal import Decimal

from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class CategoryModelTests(TestCase):
    def test_str_returns_title(self):
        cat = Category.objects.create(title='Electronics', slug='electronics')
        self.assertEqual(str(cat), 'Electronics')

    def test_slug_unique(self):
        Category.objects.create(title='A', slug='same')
        with self.assertRaises(IntegrityError):
            Category.objects.create(title='B', slug='same')


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Cat', slug='cat')

    def test_str_returns_name(self):
        p = Product.objects.create(
            name='Mouse',
            description='Wireless',
            price=Decimal('20.00'),
            inventory=3,
            category=self.category,
        )
        self.assertEqual(str(p), 'Mouse')

    def test_slug_auto_from_name_when_blank(self):
        p = Product.objects.create(
            name='USB Cable',
            description='Type C',
            price=Decimal('5.00'),
            inventory=10,
            category=self.category,
        )
        self.assertEqual(p.slug, 'usb-cable')

    def test_cannot_delete_category_referenced_by_product(self):
        Product.objects.create(
            name='X',
            description='d',
            price=Decimal('1.00'),
            inventory=1,
            category=self.category,
        )
        with self.assertRaises(ProtectedError):
            self.category.delete()


class CategoryAPITests(APITestCase):
    def test_list_categories(self):
        Category.objects.create(title='Books', slug='books')

        response = self.client.get(reverse('categories-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Books')


class ProductAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Tech', slug='tech')
        self.other = Category.objects.create(title='Home', slug='home')

    def _product(self, name, price, **extra):
        return Product.objects.create(
            name=name,
            description=f'{name} description',
            price=price,
            inventory=5,
            category=self.category,
            **extra,
        )

    def test_list_products(self):
        self._product('Laptop', Decimal('100.00'))

        response = self.client.get(reverse('products-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_product(self):
        p = self._product('Keyboard', Decimal('25.00'))

        response = self.client.get(reverse('products-detail', args=[p.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Keyboard')
        self.assertEqual(response.data['category']['slug'], 'tech')

    def test_filter_products_by_category(self):
        self._product('A', Decimal('10.00'))
        Product.objects.create(
            name='Mug',
            description='Ceramic',
            price=Decimal('8.00'),
            inventory=20,
            category=self.other,
        )

        response = self.client.get(
            reverse('products-list'),
            {'category': self.category.pk},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'A')

    def test_search_products_by_name(self):
        self._product('Laptop Pro', Decimal('1000.00'))
        self._product('Mouse', Decimal('15.00'))

        response = self.client.get(
            reverse('products-list'),
            {'search': 'Laptop'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop Pro')

    def test_order_products_by_price(self):
        self._product('Cheap', Decimal('5.00'))
        self._product('Pricey', Decimal('99.00'))

        response = self.client.get(
            reverse('products-list'),
            {'ordering': 'price'},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [row['name'] for row in response.data]
        self.assertEqual(names, ['Cheap', 'Pricey'])
