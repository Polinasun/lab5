import requests
from rest_framework.views import APIView, Response
from uuid import UUID
import logging
from .baseview import BaseView
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException

MCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 30,
     expected_exception = RequestException
)

class Menu(BaseView):
    
    URL = 'http://localhost:8003/api/menu/'
    @MCB
    def get_menu(self,request,n_uuid):
        self.info(request)
        response = requests.get(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)
    @MCB
    def patch_menu(self, request, n_uuid):
        self.info(request)
        response = requests.patch(self.URL + f'{n_uuid}', request.data)
        return Response(self.safeResponse(response), status = response.status_code)
    @MCB
    def delete_menu(self, request, n_uuid):
        self.info(request)
        response = requests.delete(self.URL + f'{n_uuid}')
        return Response(self.safeResponse(response), status = response.status_code)