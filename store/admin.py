from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'inventory', 'category', 'inventory_status']
    list_editable = ['price', 'inventory'] # ویرایش سریع قیمت از داخل لیست
    list_filter = ['category', 'created_at']
    search_fields = ['name__istartswith']
    prepopulated_fields = {'slug': ('name',)} # پر شدن خودکار اسلاگ وقتی اسم را تایپ می‌کنی

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low Stock ⚠️'
        return 'In Stock ✅'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']