from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Category, Product, Movement, Record
from .serializers import CategorySerializer, ProductSerializer, MovementSerializer, RecordSerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class MovementViewSet(viewsets.ModelViewSet):
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer

    @action(detail=False, methods=['post'])
    def compra(self, request):

        # Espera: id_user, id_product, unit_price, amount
        id_user = request.data.get('id_user')
        id_product = request.data.get('id_product')
        unit_price = request.data.get('unit_price')
        amount = request.data.get('amount')
        if not all([id_user, id_product, unit_price, amount]):
            return Response({'error': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        movement = Movement.objects.create(
            id_user_id=id_user,
            date=timezone.now().date(),
            type='compra'
        )
        Record.objects.create(
            id_movement=movement,
            id_product_id=id_product,
            unit_price=unit_price,
            amount=amount
        )
        # Se actualiza stock del producto
        product = Product.objects.get(pk=id_product)
        product.stock += float(amount)
        product.save()
        return Response({'success': 'Compra registrada.'}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def venta(self, request):

        # Espera: id_user, id_product, unit_price, amount
        id_user = request.data.get('id_user')
        id_product = request.data.get('id_product')
        unit_price = request.data.get('unit_price')
        amount = request.data.get('amount')
        if not all([id_user, id_product, unit_price, amount]):
            return Response({'error': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        movimiento = Movement.objects.create(
            id_user_id=id_user,
            date=timezone.now().date(),
            type='venta'
        )
        Record.objects.create(
            id_movement=movimiento,
            id_product_id=id_product,
            unit_price=unit_price,
            amount=amount
        )
        # Se actualiza stock del producto
        producto = Product.objects.get(pk=id_product)
        producto.stock -= float(amount)
        producto.save()
        return Response({'success': 'Venta registrada.'}, status=status.HTTP_201_CREATED)



class RecordViewSet(viewsets.ModelViewSet):
    queryset = Record.objects.all()
    serializer_class = RecordSerializer