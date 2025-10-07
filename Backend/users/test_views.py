from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()

        
        self.admin_user = self.User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="admin123",
            role="admin"
        )
        self.client.force_authenticate(user=self.admin_user)

        
        self.list_url = reverse('user-list')  

       
        self.user1 = self.User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="12345",
            role="user"
        )
        self.detail_url = reverse('user-detail', args=[self.user1.id])

    def test_list_users(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_retrieve_user(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    def test_create_user(self):
        data = {
            "username": "user2",
            "email": "user2@test.com",
            "password": "pass123",
            "role": "user"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.User.objects.filter(username="user2").exists())

    def test_update_user(self):
        data = {
            "username": "user1_updated",
            "email": "user1@test.com",
            "role": "user"
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "user1_updated")

    def test_delete_user(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.User.objects.filter(id=self.user1.id).exists())
