from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import CreateOrderSerializer, OrderSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        # این خط حیاتی است: فرستادن اطلاعات کاربر به سریالایزر
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        # هر کاربر فقط سفارش‌های خودش را ببیند
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')