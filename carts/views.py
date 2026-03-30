from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer


class CartViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # اینجا سرور خودش یوزر رو از روی توکن تشخیص میده
        cart, created = Cart.objects.get_or_create(user=request.user)

        if request.method == 'GET':
            serializer = CartSerializer(cart)
            return Response(serializer.data)

        if request.method == 'POST':
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            # اضافه کردن یا آپدیت آیتم در سبد
            item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()

            return Response({"message": "به سبد اضافه شد"}, status=201)

class CartItemViewSet(ModelViewSet):
    # فقط متدهای مورد نیاز را نگه می‌داریم
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer # این را پایین‌تر تعریف می‌کنیم
        return CartItemSerializer

    def get_serializer_context(self):
        # فرستادن cart_id به سریالایزر برای ذخیره‌سازی
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')