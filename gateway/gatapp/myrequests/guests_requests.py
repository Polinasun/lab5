import requests
from celeryQue import tasks
from rest_framework.views import APIView, Response
from uuid import UUID
import logging
from .baseview import BaseView
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException
from ..decorators import TokenHeader
from ..permissions import IsAuthenticatedByAuthenticateService
from django.conf import settings
from django.core.cache import cache


GSCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 30,
     expected_exception = RequestException
)


Tokens = TokenHeader(
    url = 'http://localhost:8002/api/guests/',
    cache = cache ,
    app_id = settings.GUEST_ID,
    app_secret = settings.GUEST_SECRET,
    t_label = 'gst'
)

class Guests(BaseView):
    
    U_GUESTS = 'http://localhost:8002/api/guests/'
    U_ROOMS = 'http://localhost:8001/api/rooms/'
    U_MENU = 'http://localhost:8003/api/menus/'
    U_GUEST = 'http://localhost:8002/api/guest/'

    
    @GSCB
    @Tokens
    def get_guests(self,request):

        flag_room = True
        flag_menu = True

        self.info(request)
        query = "?"
        params = request.query_params.dict()
        query += '&'.join([f"{key}={params[key]}" for key in params])
        response_guests = requests.get(self.U_GUESTS + query)

        guests = self.safeResponse(response_guests)

        try:
            response_rooms = requests.get(self.U_ROOMS)
        except:
            for guest in guests:
                guest['room_category'] = "Сервер не отвечает"
                flag_room = False
        
        if flag_room == True:

            rooms = self.safeResponse(response_rooms)

            for guest in guests:

                dateIsFind = False

                for room in rooms:
                    if guest['number_room'] == room['number_room']:
                        guest['room_category'] = room['category']
                        dateIsFind = True
                        break
                
                if dateIsFind == False:
                    guest['room_category'] = "Нет данных на сервере"
        
        try:
            response_menu = requests.get(self.U_MENU)
        except:
            for guest in guests:
                guest['menu_category'] = "Сервер не отвечает"
                flag_menu = False

        if flag_menu == True:

            menus = self.safeResponse(response_menu)

            for guest in guests:

                dateIsFind = False

                for menu in menus:

                    if guest['number_room'] == menu['number_room']:
                        guest['menu_category'] = menu['menu_category']
                        dateIsFind = True
                        break
                
                if dateIsFind == False:
                    guest['menu_category'] = "Нет данных на сервере"

        return Response(guests, status = response_guests.status_code)
    @GSCB
    def post_guest(self, request):
        self.info(request)
        a = request.data
        print(a)
        response = requests.post(self.U_GUESTS, request.data)
        
        room = a['number_room']

        response_guest = requests.get(self.U_GUESTS + f'?number_room={room}')
        new_guest = self.safeResponse(response_guest)
        new_guest = new_guest[0]
        guest_id = new_guest['uuid']

        try:
            response_room = requests.get(self.U_ROOMS + f'?number_room={room}',  timeout = 5)
        except:
            tasks.my_task.delay(a)
            return Response(status = "202")

        new_room = self.safeResponse(response_room)
        new_room = new_room[0]
        room_id = new_room['uuid']


        response = requests.patch(self.U_GUEST + f'{guest_id}', data = {'room_id': room_id})
        

        return Response(self.safeResponse(response), status = response.status_code)
