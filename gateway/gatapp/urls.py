from django.contrib import admin
from django.urls import path, include
from .views import RoomsView, RoomView, GuestsView, GuestView, MenusView, MenuView
from .myviews import rooms_view, room_view, guests_view, guest_view, menus_view, menu_view
urlpatterns = [
    path('rooms/', rooms_view.Rooms_View.as_view()),
    path('room/<uuid:n_uuid>', room_view.Room_View.as_view()),

    path('guests/', guests_view.Guests_View.as_view()),
    path('guest/<uuid:n_uuid>', guest_view.Guest_View.as_view()),

    path('menus/', menus_view.Menus_View.as_view()),
    path('menu/<uuid:n_uuid>', menu_view.Menu_View.as_view()),
]
