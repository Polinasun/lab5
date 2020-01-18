from .celery import app
import requests

from requests.exceptions import RequestException

@app.task(autoretry_for=(RequestException,), retry_kwargs={'max_retries': 5}, retry_backoff=True)
def my_task(a):
    
    U_GUESTS = 'http://localhost:8002/api/guests/'
    U_ROOMS = 'http://localhost:8001/api/rooms/'
    U_GUEST = 'http://localhost:8002/api/guest/'

    room = a['number_room']
    response_room = requests.get(U_ROOMS + f'?number_room={room}')
    new_room = response_room.json()
    new_room = new_room[0]
    room_id = new_room['uuid']

    response_guest = requests.get(U_GUESTS + f'?number_room={room}')
    new_guest = response_guest.json()
    new_guest = new_guest[0]
    guest_id = new_guest['uuid']

    response = requests.patch(U_GUEST + f'{guest_id}', data = {'room_id': room_id})
