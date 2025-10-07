from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Product, Movement, Record
from django.db import models

from django.contrib.auth import get_user_model
from django.utils import timezone
class MovementViewSetTest(APITestCase):
    def setUp(self):
        self.client=APIClient()
        User = get_user_model()
        self.user = User.objects.create(username="testuser",email="test@test.cl",password='12345',role="admin")
        self.client.force_authenticate(user=self.user)
       

      
        self.category = Category.objects.create(name="Categoria Test", description="Desc test")
        self.product = Product.objects.create(
            name="Producto Test",
            description="Desc producto",
            stock=10,
            unit_price=100,
            id_category=self.category  
        )

        self.compra_url = reverse('movement-compra')
        self.venta_url = reverse('movement-venta')

    def test_compra_exitosa(self):
        data = {
            "id_user": self.user.id, 
            "id_product": self.product.id_product,
            "unit_price": 120,
            "amount": 5
        }
        User = get_user_model()
        

      
        response = self.client.post(self.compra_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

       
        self.assertEqual(Movement.objects.count(), 1)
        self.assertEqual(Record.objects.count(), 1)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 15)

    def test_compra_incompleto(self):
        data = {
            "id_user": self.user.id,
        }
        response = self.client.post(self.compra_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_venta_exitosa(self):
        
        Movement.objects.create(
            id_user=self.user,  
            date=timezone.now().date(),
            type='compra'
        )

        data = {
            "id_user": self.user.id, 
            "id_product": self.product.id_product,
            "unit_price": 100,
            "amount": 3
        }

        # POST a la vista
        response = self.client.post(self.venta_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Categoria Test", description="Desc")
        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', args=[self.category.id_category])

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        data = {"name": "Nueva Categoria", "description": "Desc"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@test.cl", password='12345', role="admin")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Categoria Test", description="Desc")
        self.product1 = Product.objects.create(
            name="Producto 1", id_category=self.category, stock=0, unit_price=100
        )
        self.product2 = Product.objects.create(
            name="Producto 2", id_category=self.category, stock=5, unit_price=200
        )

        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', args=[self.product1.id_product])
        self.low_stock_url = reverse('product-low-stock')
        self.top_sold_url = reverse('product-top-sold')
        self.earnings_by_day_url = reverse('product-earnings-by-day')
        self.total_entries_url = reverse('product-total-entries')
        self.total_exits_url = reverse('product-total-exits')
        self.profit_url = reverse('product-profit')
        self.profit_percentage_url = reverse('product-profit-percentage')

        
        compra_mov = Movement.objects.create(id_user=self.user, date=timezone.now().date(), type='compra')
        Record.objects.create(id_movement=compra_mov, id_product=self.product1, unit_price=100, amount=10)

        venta_mov = Movement.objects.create(id_user=self.user, date=timezone.now().date(), type='venta')
        Record.objects.create(id_movement=venta_mov, id_product=self.product2, unit_price=200, amount=3)

   
    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        data = {
            "name": "Nuevo Producto",
            "description": "Descripción del producto",
            "id_category": self.category.id_category,
            "stock": 5,
            "unit_price": 50
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
    def test_low_stock(self):
        response = self.client.get(self.low_stock_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product1.name)

    def test_top_sold(self):
        response = self.client.get(self.top_sold_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn('id_product__name', response.data[0])
        self.assertIn('total_sold', response.data[0])

    def test_earnings_by_day(self):
        response = self.client.get(self.earnings_by_day_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(all('fecha' in d and 'ganancia' in d for d in response.data))

    def test_total_entries(self):
        response = self.client.get(self.total_entries_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['total_entries'], 0)

    def test_total_exits(self):
        response = self.client.get(self.total_exits_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['total_exits'], 0)

    def test_profit(self):
        response = self.client.get(self.profit_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profit', response.data)

    def test_profit_percentage(self):
        response = self.client.get(self.profit_percentage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profit_percentage', response.data)

class RecordViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", email="test@test.cl", password='12345', role="admin")
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Categoria Test", description="Desc")
        self.product = Product.objects.create(name="Producto Test", id_category=self.category, stock=10, unit_price=100)
        self.movement = Movement.objects.create(id_user=self.user, date=timezone.now().date(), type='compra')
        self.record = Record.objects.create(id_movement=self.movement, id_product=self.product, unit_price=100, amount=5)

        self.list_url = reverse('record-list')
        self.detail_url = reverse('record-detail', args=[self.record.id])

    def test_list_records(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_record(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.record.id)