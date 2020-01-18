from gatapp.myrequests.menu_requests import Menu
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

class Menu_View(Menu):

    def __init__(self):
        pass
    
    def get(self, request, n_uuid):
        
        try:
            response = self.get_menu(request, n_uuid)
            menu = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

       
        return Response(menu, status = code)


    def patch(self, request, n_uuid):
        
        try:
            response = self.patch_menu(request, n_uuid)
            menu = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")
            
        
        return Response(menu, status = code)


    def delete(self, request, n_uuid):

        try:
            response = self.delete_menu(request, n_uuid)
            menu = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        
        return Response(menu, status = code)