from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline): # Order ni andar items dekhadvva
    model = OrderItem
    extra = 0
    raw_id_fields = ['product'] # Large database mate performance saru rahe

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_status', 'placed_at']
    list_editable = ['payment_status']
    inlines = [OrderItemInline]
