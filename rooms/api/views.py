from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from logging import Logger
from uuid import UUID
from .serializers import room_Serializer
from .models import Rooms
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.core.exceptions import FieldError
import logging
from sys import stdout
from rest_framework.authtoken.views import ObtainAuthToken

DEFAULT_PAGE_LIMIT = settings.DEFAULT_PAGE_LIMIT

class BasView(APIView):
    logger = logging.getLogger(name='views')
    formatter = '{method} : {url} : {content_type} : {msg}'

    def info(self, request: Request, msg: str = None) -> None:
        self.logger.info(
            self.formatter.format(
                method=request.method,
                url=request._request.get_raw_uri(),
                content_type=request.content_type,
                msg=msg
            )
        )
class Room(BasView):

    def get(self, request, w_uuid: UUID):

        self.info(request)

        try:
            room_R = Rooms.objects.get(pk = w_uuid)
        except Rooms.DoesNotExist as error:
            return Response(status.HTTP_404_NOT_FOUND)
        serializer = room_Serializer(instance = room_R)
        return Response(serializer.data)


    def delete(self, request, w_uuid: UUID):

        self.info(request)

        try:
            Room_R = Rooms.objects.get(pk = w_uuid)
        except Rooms.DoesNotExist as error:
            return Response(status = status.HTTP_404_NOT_FOUND)
        Room_R.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def patch(self, request, w_uuid: UUID):

            self.info(request)

            try:
                Room_R = Rooms.objects.get(pk = w_uuid)
            except Rooms.DoesNotExist as error:
                return Response(status = status.HTTP_404_NOT_FOUND)
            serializer = room_Serializer(instance = Room_R, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Rooms_all(BasView):

    def __clear_request_params(self, request: Request) -> dict:
            params = request.query_params.dict()

            if 'page' in params: params.pop('page')
            
            return params

    def get(self, request):
        self.info(request)
        params = self.__clear_request_params(request)

        try:
            Room_R = Rooms.objects.filter(**params)

        except FieldError as error:
            return Response(status = status.HTTP_400_BAD_REQUEST )

        paginator = PageNumberPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        page = paginator.paginate_queryset(Room_R, request)

        serializer = room_Serializer(Room_R, many = True)
        return Response(data = serializer.data)

    def post(self, request):

        self.info(request)

        serializer = room_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)

        return Response(status = status.HTTP_400_BAD_REQUEST, data="BAD REQUEST")

        
class CustomObtainTokenView(BaseView, ObtainAuthToken):
    permission_classes = []
    authentication_classes = []
    serializer_class = AppAuthSerializer
    def post(self, request: Request) -> Response:
        self.info(request)
        
        serializer = self.serializer_class(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception = True)
        token = CustomToken.objects.create()

        return Response(data = {'token': token.token}, status = status.HTTP_200_OK)
