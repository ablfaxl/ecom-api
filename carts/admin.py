from django.contrib import admin
from .models import Cart,CartItem



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_filter = ['created_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity']
    list_editable = ['quantity']
    list_filter = ['cart__created_at']
    search_fields = ['product__name']
    raw_id_fields = ['cart', 'product']