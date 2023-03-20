import base64
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Photo, Tier

User = get_user_model()

class PhotoTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tier = Tier.objects.create(name='Basic', thumbnail_200px=True, source_image=True)
        self.user = User.objects.create_user(username='testuser', password='testpass', tier=self.tier)
        self.photo = Photo.objects.create(
            owner=self.user,
            source_image="source\\test.png"
        )

    def test_create_photo(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/photos/', {'source_image': self.photo.source_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('source_image' in response.data)
        self.assertTrue('thumbnail_200px' in response.data)

    def test_list_photos(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('source_image' in response.data[0])
        self.assertTrue('thumbnail_200px' in response.data[0])

    def test_create_expiring_link(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/links/', {'image': self.photo.id, 'expiration_time': 3600})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('detail' in response.data)
        expiring_link = response.data['detail']
        self.assertTrue(expiring_link.startswith('http'))
        self.assertTrue(str(self.photo.id) in expiring_link)

    def test_retrieve_expiring_link(self):
        self.client.force_login(self.user)
        expiration_time = 3600
        expiring_link = self.create_expiring_link(self.photo, expiration_time)
        response = self.client.get(expiring_link)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_retrieve_expired_expiring_link(self):
        self.client.force_login(self.user)
        expiration_time = 0
        expiring_link = self.create_expiring_link(self.photo, expiration_time)
        response = self.client.get(expiring_link)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def create_expiring_link(self, photo, expiration_time):
        expiration_datetime = datetime.now() + timedelta(seconds=expiration_time)
        expiring_link = Photo.expiring_links.create(photo=photo, expiration_datetime=expiration_datetime)
        return expiring_link.link
