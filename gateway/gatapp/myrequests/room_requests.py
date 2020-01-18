import requests
from rest_framework.views import APIView, Response
from uuid import UUID
import logging
from .baseview import BaseView
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException


RCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 30,
     expected_exception = RequestException
)

class Room(BaseView):
    
    URL = 'http://localhost:8001/api/room/'
    URL1 = 'http://localhost:8002/api/guest/'
    URL2 ='http://localhost:8003/api/menus/'

    @RCB
    def get_room(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

    @RCB
    def patch_room(self, request, n_uuid):
        self.info(request)
        response = requests.patch(self.URL + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)

    @RCB
    def delete_room(self, request, n_uuid):
        self.info(request)

        response = requests.get(self.URL1 + f'?room_id = {n_uuid}')
        re_room = self.safeResponse(response)

        if response.status_code == 200:
        
            re_room = re_room[0]
            re_guest = re_room['bed1']
            response = requests.patch(self.URL1 + f'{re_guest}', data = {'room_id': UUID(int = 0)})

        response = requests.get(self.URL2 + f'?room_id = {n_uuid}')
        rest_guest = self.safeResponse(response)

        if response.status_code == 200:

            re_menu = re_room['bed1']
            response = requests.patch(self.URL2 + f'{re_menu}', data = {'room_id': UUID(int = 0)})


        response = requests.delete(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

