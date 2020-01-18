from gatapp.myrequests.room_requests import Room
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

class Room_View(Room):


    def __init__(self):
        pass
    
    def get(self, request, n_uuid):
        
        try:
            response = self.get_room(request, n_uuid)

            room = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")


        
        return Response(room, status = code)


    def patch(self, request, n_uuid):
        
        try:
            response = self.patch_room(request, n_uuid)

            room = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        
        return Response(room, status = code)


    def delete(self, request, n_uuid):

        try:
            response = self.delete_room(request, n_uuid)

            room = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        
        return Response(room, status = code)
