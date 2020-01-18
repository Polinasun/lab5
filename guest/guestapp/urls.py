from django.urls import path
from .views import *
urlpatterns = [
    path('guests/', Guests_all.as_view()),
    path('guest/<uuid:w_uuid>', Guest.as_view())
]
