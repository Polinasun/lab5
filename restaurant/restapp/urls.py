from django.urls import path
from .views import *
urlpatterns = [
    path('menus/', Menus_all.as_view()),
    path('menu/<uuid:w_uuid>', Menu_1.as_view())
]
