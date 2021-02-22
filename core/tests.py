# from .views import  CategoryListView, CategoryCreateView
from rest_framework import status
from rest_framework.test import APITestCase


class ItemTestCase(APITestCase):
    def setUp(self):
        self.category_url = '/api/categories/'
        self.category_data = [{"type": "test1"}, {"type": "test2"}, {"type": "test3"}]
        for cat in self.category_data:
            self.client.post(self.category_url, cat, format='json')
        self.product_url = '/api/products/'
        self.product_data = {
                                "name": "Test product1",
                                "price": 1,
                                "is_published": "true",
                                "categories": [1, 2],
                                "is_deleted": "false"
                            }

    def test_1category_delete_not_empty(self):
        self.client.post(self.product_url, self.product_data, format='json')
        response = self.client.delete(f'{self.category_url}test1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_creation(self):
        data = {"type": "test4"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_duplicated_entry_error(self):
        data = {"type": "test3"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_duplicated_entry_error2(self):
        data = {"type": "test3"}
        response = self.client.post(self.category_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_delete(self):
        response = self.client.delete(f'{self.category_url}test1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

