from gatapp.myrequests.guests_requests import Guests
import requests
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from uuid import UUID
import logging
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

class Guests_View(Guests):

    #permission_classes = (IsAuthenticated,) # напсать

    def __init__(self):
        pass
    
    def get(self, request):
        
        try:
            response = self.get_guests(request)
            guests = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = 500)


        
        return Response(guests, status = code)


    def post(self, request):
        
        try:
            response = self.post_guest(request)
            guest = response.data
            code = response.status_code

        except CircuitBreakerError:
            return Response(status = 500)

        
        return Response(guest, status = code)
