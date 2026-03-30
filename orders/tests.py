from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Category

class ProductTest(APITestCase):
    def test_get_all_products(self):
        # ۱. آماده‌سازی دیتا
        category = Category.objects.create(title='Tech', slug='tech')
        Product.objects.create(name='Laptop', price=100, inventory=5, category=category)
        
        # ۲. ارسال درخواست به API
        response = self.client.get('/api/v1/store/products/')
        
        # ۳. چک کردن نتیجه
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)