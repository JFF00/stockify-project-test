from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from django.db.models import Sum, F, FloatField


from django.utils import timezone
from .models import Category, Product, Movement, Record
from .serializers import CategorySerializer, ProductSerializer, MovementSerializer, RecordSerializer

# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # 🔹 Total de categorías y listado de nombres
    @action(detail=False, methods=['get'])
    def summary(self, request):
        categories = Category.objects.all().values('id_category', 'name')
        total = categories.count()
        return Response({
            'total_categories': total,
            'categories': list(categories)
        }, status=status.HTTP_200_OK)
    
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
    
    # 🔹 Lista de productos con su cantidad en stock
    @action(detail=False, methods=['get'])
    def stock(self, request):
        products = Product.objects.all().values('id_product', 'name', 'stock')
        return Response(list(products), status=status.HTTP_200_OK)

    # 🔹 Valor total del stock
    @action(detail=False, methods=['get'])
    def stock_value(self, request):
        total_value = Product.objects.aggregate(
            total_value=Sum(F('stock') * F('unit_price'), output_field=FloatField())
        )['total_value'] or 0.0
        return Response({'total_value': round(total_value, 2)}, status=status.HTTP_200_OK)

    # Productos sin movimiento (nunca registraron Record)
    @action(detail=False, methods=['get'])
    def no_movement(self, request):
        qs = (Product.objects
            .filter(record__isnull=True)          
            .values('id_product', 'name', 'stock'))
        return Response(list(qs), status=status.HTTP_200_OK)

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
            .annotate(ganancia=Sum(F('unit_price') * F('amount'), output_field=FloatField()))
            .order_by('id_movement__date')
        )
        resultado = [
            {
                'fecha': g['id_movement__date'],
                'ganancia': float(g['ganancia']) if g['ganancia'] is not None else 0.0
            }
            for g in ganancias
        ]
        return Response(resultado, status=status.HTTP_200_OK)

    # Total entradas (Purchases)
    @action(detail=False, methods=['get'])
    def total_entries(self, request):
        total = Record.objects.filter(id_movement__type='compra').aggregate(
            total_entries=Sum(F('unit_price') * F('amount'), output_field=FloatField())
        )['total_entries'] or 0.0
        return Response({'total_entries': float(total)}, status=status.HTTP_200_OK)

    # Total Exits (Sales)
    @action(detail=False, methods=['get'])
    def total_exits(self, request):
        total = Record.objects.filter(id_movement__type='venta').aggregate(
            total_exits=Sum(F('unit_price') * F('amount'), output_field=FloatField())
        )['total_exits'] or 0.0
        return Response({'total_exits': float(total)}, status=status.HTTP_200_OK)

    # Profit (Sales - Purchases)
    @action(detail=False, methods=['get'])
    def profit(self, request):
        total_sales = Record.objects.filter(id_movement__type='venta').aggregate(
            total=Sum(F('unit_price') * F('amount'), output_field=FloatField())
        )['total'] or 0.0
        total_purchases = Record.objects.filter(id_movement__type='compra').aggregate(
            total=Sum(F('unit_price') *F('amount'), output_field=FloatField())
        )['total'] or 0.0
        profit = total_sales - total_purchases
        return Response({'profit': float(profit)}, status=status.HTTP_200_OK)

    # Profit Percentage
    @action(detail=False, methods=['get'])
    def profit_percentage(self, request):
        total_sales = Record.objects.filter(id_movement__type='venta').aggregate(
            total=Sum(F('unit_price') * F('amount'), output_field=FloatField())
        )['total'] or 0.0
        total_purchases = Record.objects.filter(id_movement__type='compra').aggregate(
            total=Sum(F('unit_price') *F('amount'), output_field=FloatField())
        )['total'] or 0.0
        profit = total_sales - total_purchases
        percentage = (profit / total_sales * 100) if total_sales > 0 else 0.0
        return Response({'profit_percentage': round(percentage, 2)}, status=status.HTTP_200_OK)

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