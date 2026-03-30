from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem
from carts.models import Cart, CartItem
from store.models import Product


class CreateOrderSerializer(serializers.Serializer):
    # دقت کن: فیلد cart_id کلاً حذف شد چون سرور خودش پیدایش می‌کند

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id']

            # ۱. پیدا کردن سبد خرید متعلق به این کاربر
            try:
                cart = Cart.objects.get(user_id=user_id)
                cart_items = CartItem.objects.select_related('product').filter(cart=cart)
            except Cart.DoesNotExist:
                raise serializers.ValidationError('سبد خریدی برای این کاربر یافت نشد.')

            if not cart_items.exists():
                raise serializers.ValidationError('سبد خرید شما خالی است.')

            # ۲. چک کردن موجودی انبار برای تمام محصولات سبد
            for item in cart_items:
                if item.product.inventory < item.quantity:
                    raise serializers.ValidationError(
                        f'موجودی محصول {item.product.name} کافی نیست. (موجودی فعلی: {item.product.inventory})'
                    )

            # ۳. ساخت رکورد اصلی سفارش (Order)
            order = Order.objects.create(user_id=user_id)

            # ۴. انتقال آیتم‌ها و بروزرسانی انبار
            order_items = []
            for item in cart_items:
                # کم کردن از موجودی محصول در دیتابیس
                product = item.product
                product.inventory -= item.quantity
                product.save()

                # ساخت آبجکت OrderItem (هنوز در دیتابیس ذخیره نمی‌شود)
                order_items.append(OrderItem(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    unit_price=product.price  # قیمت لحظه خرید ذخیره می‌شود
                ))

            # ۵. ذخیره دسته‌جمعی تمام آیتم‌ها (بهینه برای دیتابیس)
            OrderItem.objects.bulk_create(order_items)

            # ۶. خالی کردن سبد خرید کاربر پس از ثبت موفق سفارش
            cart_items.delete()

            return order


class OrderItemSerializer(serializers.ModelSerializer):
    # برای نمایش در لیست سفارشات
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'items']