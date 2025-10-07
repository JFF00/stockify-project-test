from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product, Movement, Record
from django.utils import timezone

class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Test Category", description="Desc")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Desc")
        self.assertIsNotNone(category.created_at)
        self.assertTrue(isinstance(category.id_category, int))

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Cat 1", description="Desc")

    def test_create_product(self):
        product = Product.objects.create(
            name="Prod 1",
            description="Desc prod",
            stock=10,
            unit_price=100.50,
            id_category=self.category
        )
        self.assertEqual(product.name, "Prod 1")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.unit_price, 100.50)
        self.assertEqual(product.id_category, self.category)
        self.assertIsNotNone(product.created_at)

class MovementModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user1", email="a@b.com", password="12345")
    
    def test_create_movement(self):
        movement = Movement.objects.create(
            id_user=self.user,
            date=timezone.now().date(),
            type="compra"
        )
        self.assertEqual(movement.id_user, self.user)
        self.assertEqual(movement.type, "compra")
        self.assertIsNotNone(movement.date)

class RecordModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="user1", email="a@b.com", password="12345")
        self.category = Category.objects.create(name="Cat 1", description="Desc")
        self.product = Product.objects.create(
            name="Prod 1", description="Desc", stock=5, unit_price=100, id_category=self.category
        )
        self.movement = Movement.objects.create(
            id_user=self.user, date=timezone.now().date(), type="compra"
        )

    def test_create_record(self):
        record = Record.objects.create(
            id_movement=self.movement,
            id_product=self.product,
            unit_price=150,
            amount=3
        )
        self.assertEqual(record.id_movement, self.movement)
        self.assertEqual(record.id_product, self.product)
        self.assertEqual(record.unit_price, 150)
        self.assertEqual(record.amount, 3)
