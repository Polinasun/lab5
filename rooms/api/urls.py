from django.urls import path
from .views import *
urlpatterns = [
    path('rooms/', Rooms_all.as_view()),
    path('room/<uuid:w_uuid>', Room.as_view()),
    path('auth/', CustomObtainTokenView.as_view())
]
