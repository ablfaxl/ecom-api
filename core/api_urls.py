from django.urls import path, include
from rest_framework_nested import routers
from store.views import ProductViewSet, CategoryViewSet

from carts.views import CartViewSet, CartItemViewSet
from orders.views import OrderViewSet

# ۱. تعریف روتر اصلی
router = routers.DefaultRouter()

# مسیرهای اپلیکیشن Store
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')

# مسیرهای اپلیکیشن Carts
router.register('carts', CartViewSet, basename='carts')

# مسیرهای اپلیکیشن Orders
router.register('orders', OrderViewSet, basename='orders')

# ۲. تعریف روتر تو در تو (Nested) برای آیتم‌های سبد خرید
# این باعث می‌شه آدرس بشه: /carts/{cart_pk}/items/
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

# ۳. تجمیع تمام URLها
urlpatterns = [
    # مسیرهای اتوماتیک روترها
    path('', include(router.urls)),
    path('', include(carts_router.urls)),

    # مسیرهای اپلیکیشن Accounts (احراز هویت)
    path('auth/', include('djoser.urls')),  # اگر از Djoser استفاده می‌کنی
    path('auth/', include('djoser.urls.jwt')),  # برای Token Obtain/Refresh
]