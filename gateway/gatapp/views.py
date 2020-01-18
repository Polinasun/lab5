from django.shortcuts import render
from rest_framework.views import APIView, Response
from uuid import UUID
import requests
import logging

class BaseView(APIView):
    logger = logging.getLogger(name = 'views')
    formatter = '{method} : {url} : {content_type} : {msg}'

    def info(self, request, msg = None):
        self.logger.info(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )

    def exception(self, request, msg = None):
        self.logger.exception(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )
    def safeResponse(self,response):
        try:
            return response.json()

        except ValueError as error:
            #self.exception()
            return response.text

class RoomsView(BaseView):

    URL = 'http://localhost:8001/api/rooms/'

    def get(self,request):
        self.info(request)
        query = "?"
        params = request.query_params.dict()
        query += '&'.join([f"{key}={params[key]}" for key in params])
        response = requests.get(self.URL + query)
        return Response(self.safeResponse(response), status = response.status_code)

    def post(self, request):
        self.info(request)
        response = requests.post(self.URL, request.data)
        return Response(self.safeResponse(response), status = response.status_code)

class RoomView(BaseView):

    URL = 'http://localhost:8001/api/room/'
    URL1 = 'http://localhost:8002/api/guest/'
    URL2 ='http://localhost:8003/api/menus/'

    def get(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

    def patch(self, request, n_uuid):
        self.info(request)
        response = requests.patch(self.URL + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)

    def delete(self, request, n_uuid):
        self.info(request)

        response = requests.get(self.URL1 + f'?room_id = {n_uuid}')
        re_room = self.safeResponse(response)

        re_guest = re_room['bed1']
        response = requests.patch(self.URL1 + f'{re_guest}', data = {'room_id': UUID(int = 0)})

        response = requests.get(self.URL2 + f'?room_id = {n_uuid}')
        rest_guest = self.safeResponse(response)

        re_menu = re_room['bed1']
        response = requests.patch(self.URL2 + f'{re_menu}', data = {'room_id': UUID(int = 0)})


        response = requests.delete(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

class GuestsView(BaseView):

    U_GUESTS = 'http://localhost:8002/api/guests/'
    U_ROOMS = 'http://localhost:8001/api/rooms/'
    U_MENU = 'http://localhost:8003/api/menus/'
    

    def get(self,request):

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

    def post(self, request):
        self.info(request)
        a = request.data
        print(a)
        response = requests.post(self.U_GUESTS, request.data)

        return Response(self.safeResponse(response), status = response.status_code)

class GuestView(BaseView):


    URL1 ='http://localhost:8001/api/room/'
    URL1_1 = 'http://localhost:8001/api/rooms/'
    URL = 'http://localhost:8002/api/guest/'
    URL2_2 ='http://localhost:8003/api/menus/'
    URL2 ='http://localhost:8003/api/menu/'

    def get(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL + f'{n_uuid}')

        return Response(self.safeResponse(response), status = response.status_code)


    def patch(self, request, n_uuid):

        self.info(request)
        response = requests.patch(self.URL + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)

    def delete(self, request, n_uuid):
        self.info(request)


        response = requests.get(self.URL1_1 + f'?bed1={n_uuid}')
        re_guest = self.safeResponse(response)

        print(re_guest)


        re_room = re_guest[0]
        re_room = re_room['uuid']
        response = requests.patch(self.URL1 + f'{re_room}', data = {'bed1': UUID(int = 0)})


        response = requests.get(self.URL2_2 + f'?room_id={re_room}')
        re_guest = self.safeResponse(response)

       
        re_menu = re_guest[0]
        re_menu = re_menu['uuid']
        response = requests.patch(self.URL2 + f'{re_menu}', data = {'room_id': UUID(int = 0)})


        response = requests.delete(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

class MenusView(BaseView):

    URL = 'http://localhost:8003/api/menus/'

    def get(self,request):
        self.info(request)
        query = "?"
        params = request.query_params.dict()
        query += '&'.join([f"{key}={params[key]}" for key in params])
        response = requests.get(self.URL + query)
        return Response(self.safeResponse(response), status = response.status_code)

    def post(self, request):
        self.info(request)
        response = requests.post(self.URL, request.data)
        return Response(self.safeResponse(response), status = response.status_code)

class MenuView(BaseView):

    URL = 'http://localhost:8001/api/menu/'

    def get(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)

    def patch(self, request, n_uuid):
        self.info(request)
        response = requests.patch(self.URL + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)

    def delete(self, request, n_uuid):
        self.info(request)
        response = requests.delete(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)
