from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate, APITestCase
from .models import Rooms
import json
from uuid import uuid4

class Rooms_Tests(APITestCase):

    url = '/api/rooms/'

    def test_Post(self):

        room_T = {
            'number_room': 1408,
            'category': '0',
            'bed1': 0
            }

        response = self.client.post(self.url, room_T, format = 'json')
        self.assertEqual(201, response.status_code)

    def test_Get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class Room_Tests(APITestCase):

    url = '/api/room/'

    def setUp(self):

        self.number_room = 1408
        self.category = "0"
        self.bed1 = 0

        self.Room, created = Rooms.objects.get_or_create(
            number_room = self.number_room,
            category = self.category,
            bed1 = self.bed1
        )


    def test_Get_One(self):
        print(self.Room.uuid)
        uuid_T = self.Room.uuid
        response = self.client.get(self.url + f'{uuid_T}')
        self.assertEqual(200, response.status_code)


    def test_Patch(self):

        self.Room, created = Rooms.objects.get_or_create(
            number_room = self.number_room,
            category = self.category,
            bed1 = self.bed1
        )

        uuid_T = self.Room.uuid

        room_P = {
            'number_room' : self.number_room,
            'category' : "1",
            'bed1' : self.bed1
        }

        response = self.client.patch(self.url + f'{uuid_T}', data = room_P, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_Delete(self):

        uuid_T = self.Room.uuid
        response = self.client.delete(self.url + f'{uuid_T}')
        self.assertEqual(204, response.status_code)
