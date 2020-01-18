from gatapp.myrequests.rooms_requests import Rooms
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

class Rooms_View(Rooms):


    def __init__(self):
        pass
    
    def get(self, request):
        
        try:
            response = self.get_rooms(request)
            rooms = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")


        
        return Response(rooms, status = code)


    def post(self, request):
        
        try:
            response = self.post_rooms(request)

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        room = response.data
        code = response.status_code

        return Response(room, status = code)