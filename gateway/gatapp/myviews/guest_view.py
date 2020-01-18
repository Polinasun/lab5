from gatapp.myrequests.guest_requests import Guest
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

class Guest_View(Guest):
    #permission_classes = (IsAuthenticated,) # напсать

    def __init__(self):
        pass
    
    def get(self, request, n_uuid):
        
        try:
            response = self.get_guest(request, n_uuid)
            guest = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        # if response.is

        
        return Response(guest, status = code)


    def patch(self, request, n_uuid):
        
        try:
            response = self.patch_guest(request, n_uuid)
            guest = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")

        
        return Response(guest, status = code)


    def delete(self, request, n_uuid):

        try:
            response = self.delete_guest(request, n_uuid)
            guest = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = "500 Internal Server Error")
            

        
        return Response(guest, status = code)
