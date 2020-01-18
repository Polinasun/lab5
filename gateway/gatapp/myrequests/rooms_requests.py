import requests
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

RSCB = CircuitBreaker(
    failure_threshold = 5,
    recovery_timeout = 30,
     expected_exception = RequestException
)

Tokens = TokenHeader(
    url = 'http://localhost:8002/api/auth/',
    cache = cache ,
    app_id = settings.GUEST_ID,
    app_secret = settings.GUEST_SECRET,
    t_label = 'gst'
)

class Rooms(BaseView):
    
    URL = 'http://localhost:8001/api/rooms/'
    
    @RSCB
    @Tokens
    def get_rooms(self,request):
        self.info(request)
        query = "?"
        params = request.query_params.dict()
        query += '&'.join([f"{key}={params[key]}" for key in params])
        response = requests.get(self.URL + query)
        return Response(self.safeResponse(response), status = response.status_code)
    @RSCB
    def post_rooms(self, request):
        self.info(request)
        response = requests.post(self.URL, request.data)
        return Response(self.safeResponse(response), status = response.status_code)