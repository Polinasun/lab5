import requests
from rest_framework.views import APIView, Response
from uuid import UUID
import logging
from .baseview import BaseView
from circuitbreaker import CircuitBreaker, CircuitBreakerError
from requests.exceptions import RequestException



MSCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 30,
     expected_exception = RequestException
)


class Menus(BaseView):
    
    URL = 'http://localhost:8003/api/menus/'
    @MSCB
    def get_menus(self,request):
        self.info(request)
        query = "?"
        params = request.query_params.dict()
        query += '&'.join([f"{key}={params[key]}" for key in params])
        response = requests.get(self.URL + query)
        return Response(self.safeResponse(response), status = response.status_code)
    @MSCB
    def post_menu(self, request):
        self.info(request)
        response = requests.post(self.URL, request.data)
        return Response(self.safeResponse(response), status = response.status_code)