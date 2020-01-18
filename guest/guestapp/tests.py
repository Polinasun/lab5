from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, force_authenticate, APITestCase
from .models import Guests
import json
from uuid import uuid4

class Guests_Tests(APITestCase):

    url = '/api/guests/'

    def test_Post(self):

        guest_T = {
            'name':'Mark',
            'surname':'Smith',
            'number_room': 1408,
            'room_id': 0
            }

        response = self.client.post(self.url, guest_T, format = 'json')
        self.assertEqual(201, response.status_code)

    def test_Get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)


class Guest_Tests(APITestCase):

    url = '/api/guest/'

    def setUp(self):

        self.name = 'Nike'
        self.surname = 'Jordan'
        self.number_room = 1408
        self.room_id = 0

        self.Guest, created = Guests.objects.get_or_create(
            name = self.name,
            surname = self.surname,
            number_room = self.number_room,
            room_id = self.room_id
        )


    def test_Get_One(self):
        print(self.Guest.uuid)
        uuid_T = self.Guest.uuid
        response = self.client.get(self.url + f'{uuid_T}')
        self.assertEqual(200, response.status_code)


    def test_Patch(self):

        self.Guest, created = Guests.objects.get_or_create(
            name = self.name,
            surname = self.surname,
            number_room = self.number_room,
            room_id = self.room_id
        )

        uuid_T = self.Guest.uuid

        guest_P = {
            'name': self.name,
            'surname': self.surname,
            'number_room' : self.number_room,
            'room_id' : 0
        }

        response = self.client.patch(self.url + f'{uuid_T}', data = guest_P, format = 'json')

        self.assertEqual(202, response.status_code)

    def test_Delete(self):

        uuid_T = self.Guest.uuid
        response = self.client.delete(self.url + f'{uuid_T}')
        self.assertEqual(204, response.status_code)
