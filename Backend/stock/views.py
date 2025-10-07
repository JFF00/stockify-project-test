from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.db.models import Sum
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

    # Productos sin stock
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        # Muestra solo los productos con stock = 0
        products = Product.objects.filter(stock__lte=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Productos más vendidos
    @action(detail=False, methods=['get'])
    def top_sold(self, request):
        period = request.query_params.get('period', 'todo')  # mes | año | todo
        now = timezone.now()
        records = Record.objects.select_related('id_product', 'id_movement')

        if period == 'mes':
            records = records.filter(id_movement__date__year=now.year, id_movement__date__month=now.month)
        elif period == 'año':
            records = records.filter(id_movement__date__year=now.year)
        # 'todo' => sin filtro de fecha

        top = (
            records.values('id_product__name')
            .annotate(total_sold=Sum('amount'))
            .order_by('-total_sold')[:10]  # El top 10 de los productos mas vendidos
        )
        return Response(top, status=status.HTTP_200_OK)

    # Ganancias por día
    @action(detail=False, methods=['get'])
    def earnings_by_day(self, request):
        records = Record.objects.filter(id_movement__type='venta')
        ganancias = (
            records.values('id_movement__date')
            .annotate(ganancia=Sum(models.F('unit_price') * models.F('amount')))
            .order_by('id_movement__date')
        )
        resultado = [
            {
                'fecha': g['id_movement__date'],
                'ganancia': float(g['ganancia']) if g['ganancia'] is not None else 0.0
            }
            for g in ganancias
        ]
        return Response(resultado, status=status.HTTP_200_OK)'

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