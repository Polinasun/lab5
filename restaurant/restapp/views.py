from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView, Request, Response
from logging import Logger
from uuid import UUID
from .serializers import menu_Serializer
from .models import Menu
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.core.exceptions import FieldError
import logging
from sys import stdout

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
class Menu_1(BasView):

    def get(self, request, w_uuid: UUID):

        self.info(request)

        try:
            menu_R = Menu.objects.get(pk = w_uuid)
        except Menu.DoesNotExist as error:
            return Response(status.HTTP_404_NOT_FOUND)
        serializer =menu_Serializer(instance = menu_R)
        return Response(serializer.data)


    def delete(self, request, w_uuid: UUID):

        self.info(request)

        try:
            menu_R = Menu.objects.get(pk = w_uuid)
        except Menu.DoesNotExist as error:
            return Response(status = status.HTTP_404_NOT_FOUND)
        menu_R.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

    def patch(self, request, w_uuid: UUID):

            self.info(request)

            try:
                menu_R = Menu.objects.get(pk = w_uuid)
            except Menu.DoesNotExist as error:
                return Response(status = status.HTTP_404_NOT_FOUND)
            serializer = menu_Serializer(instance = menu_R, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)
            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Menus_all(BasView):

    def __clear_request_params(self, request: Request) -> dict:
            params = request.query_params.dict()

            if 'page' in params: params.pop('page')

            return params

    def get(self, request):
        self.info(request)
        params = self.__clear_request_params(request)

        try:
            menu_R = Menu.objects.filter(**params)

        except FieldError as error:
            return Response(status = status.HTTP_400_BAD_REQUEST )

        paginator = PageNumberPagination()
        paginator.default_limit = DEFAULT_PAGE_LIMIT
        page = paginator.paginate_queryset(menu_R, request)

        serializer = menu_Serializer(menu_R, many = True)
        return Response(data = serializer.data)

    def post(self, request):

        self.info(request)

        serializer = menu_Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)

        return Response(status = status.HTTP_400_BAD_REQUEST)
