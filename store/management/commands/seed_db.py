import random
from django.core.management.base import BaseCommand
from store.models import Product, Category

class Command(BaseCommand):
    help = 'پیمانه کردن دیتابیس با داده‌های تستی'

    def handle(self, *args, **options):
        self.stdout.write('در حال پاکسازی دیتابیس قدیمی...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('در حال ساخت داده‌های جدید...')

        # ۱. ساخت دسته‌بندی‌ها
        categories = ['لپ‌تاپ', 'گوشی هوشمند', 'اکسسوری', 'قطعات کامپیوتر']
        cat_objects = []
        for name in categories:
            cat = Category.objects.create(title=name, slug=name.replace(' ', '-'))
            cat_objects.append(cat)

        # ۲. ساخت محصولات تستی
        products_data = [
            ('MacBook Pro M3', 1200, 10),
            ('iPhone 15 Pro', 999, 15),
            ('Samsung S24 Ultra', 1100, 8),
            ('AirPods Pro', 250, 50),
            ('Keychron K2', 120, 30),
            ('Logitech MX Master 3S', 99, 40),
            ('Dell XPS 15', 1500, 5),
            ('Sony WH-1000XM5', 350, 20),
        ]

        for name, price, inv in products_data:
            Product.objects.create(
                name=name,
                price=price,
                inventory=inv,
                category=random.choice(cat_objects),
                description=f"این یک توضیحات تستی برای محصول {name} است."
            )

        self.stdout.write(self.style.SUCCESS('هورا! دیتابیس با موفقیت Seed شد.'))