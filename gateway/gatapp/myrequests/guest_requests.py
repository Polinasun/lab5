import requests
from rest_framework.views import APIView, Response
from uuid import UUID
import logging
from .baseview import BaseView
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

GCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 60,
    expected_exception = RequestException
)

class Guest(BaseView):

    URL_ROOM ='http://localhost:8001/api/room/'
    URL_ROOMS = 'http://localhost:8001/api/rooms/'
    URL_GUEST = 'http://localhost:8002/api/guest/'
    URL_MENUS ='http://localhost:8003/api/menus/'
    URL_MENU ='http://localhost:8003/api/menu/'

    @GCB
    def get_guest(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL_GUEST + f'{n_uuid}', timeout = 4)

        return Response(self.safeResponse(response), status = response.status_code)

    @GCB
    def patch_guest(self, request, n_uuid):

        self.info(request)
        response = requests.patch(self.URL_GUEST + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)

    @GCB
    def delete_guest(self, request, n_uuid):
        self.info(request)

        response = requests.get(self.URL_ROOMS + f'?bed1={n_uuid}')
        guests_room = self.safeResponse(response)



        if not (len(guests_room) == 0):
            re_room = guests_room[0]
            re_room = re_room['uuid']
            response = requests.patch(self.URL_ROOM + f'{re_room}', data = {'bed1': UUID(int = 0)})

            if response.status_code != 202:
                return Response(self.safeResponse(response), status = response.status_code)
        
    

            response = requests.get(self.URL_MENUS + f'?room_id={re_room}')
            re_guest = self.safeResponse(response)
        


            if not (len(re_guests) == 0):
                re_menu = re_guest[0]
                re_menu = re_menu['uuid']
                response = requests.patch(self.URL_MENU + f'{re_menu}', data = {'room_id': UUID(int = 0)})

                if response.status_code != 202:
                    response_reboot = requests.patch(self.URL_ROOM + f'{re_room}', data = {'bed1': n_uuid})
                    return Response(self.safeResponse(response), status = response.status_code)
                    
        response = requests.delete(self.URL_GUEST + f'{n_uuid}')

        if response.status_code != 204:
            response_reboot= requests.patch(self.URL_ROOM + f'{re_room}', data = {'bed1': n_uuid})
            response_reb= requests.patch(self.URL_MENU + f'{re_menu}', data = {'room_id': re_room})
            return Response(self.safeResponse(response), status = response.status_code)



        return Response(self.safeResponse(response), status = response.status_code)

