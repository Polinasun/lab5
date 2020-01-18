from gatapp.myrequests.menus_requests import Menus
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException




class Menus_View(Menus):


    def __init__(self):
        pass

    def get(self, request):
        
        try:
            response = self.get_menus(request)
            menu = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        return Response(menu , status = code)


    def post(self, request):
        
        try:
            response = self.post_menu(request)
            menu = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")


        return Response(menu, status = code)
