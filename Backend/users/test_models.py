from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create(
            username="testuser",
            email="test@test.com",
            password="12345",
            role="user"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@test.com")
        self.assertEqual(user.role, "user")
        self.assertIsNotNone(user.id)  

    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="admin123"
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_str_method(self):
        user = self.User.objects.create(username="john", email="john@test.com")
        self.assertEqual(str(user), "john") 

    def test_user_role_default(self):
        user = self.User.objects.create(username="roleuser", email="role@test.com", password="123")
        self.assertEqual(user.role, "user")  
