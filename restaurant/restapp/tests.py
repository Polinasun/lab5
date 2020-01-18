from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate, APITestCase
from .models import Menu
import json
from uuid import uuid4

class Menus_Tests(APITestCase):

    url = '/api/menus/'

    def test_Post(self):

        menu_T = {
            'number_room': 1408,
            'menu_category': '0',
            'room_id': 0
            }

        response = self.client.post(self.url, menu_T, format = 'json')
        self.assertEqual(201, response.status_code)

    def test_Get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class Menu_Tests(APITestCase):

    url = '/api/menu/'

    def setUp(self):

        self.number_room = 1408
        self.menu_category = "0"
        self.room_id = 0

        self.Menu_1, created = Menu.objects.get_or_create(
            number_room = self.number_room,
            menu_category = self.menu_category,
            room_id = self.room_id
        )


    def test_Get_One(self):
        print(self.Menu_1.uuid)
        uuid_T = self.Menu_1.uuid
        response = self.client.get(self.url + f'{uuid_T}')
        self.assertEqual(200, response.status_code)


    def test_Patch(self):

        self.Menu_1, created = Menu.objects.get_or_create(
            number_room = self.number_room,
            menu_category = self.menu_category,
            room_id = self.room_id
        )

        uuid_T = self.Menu_1.uuid

        menu_P = {
            'number_room' : self.number_room,
            'menu_category' : "1",
            'room_id' : self.room_id
        }

        response = self.client.patch(self.url + f'{uuid_T}', data = menu_P, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_Delete(self):

        uuid_T = self.Menu_1.uuid
        response = self.client.delete(self.url + f'{uuid_T}')
        self.assertEqual(204, response.status_code)
