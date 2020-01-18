from django.db import models
from uuid import uuid4
#from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class Guests(models.Model):

    name = models.CharField(max_length = 30)
    surname = models.CharField(max_length = 30)
    number_room=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(500)])
    room_id = models.UUIDField(default = uuid4)
    uuid = models.UUIDField(primary_key = True, default = uuid4)


    def __str__(self):
        return self.title
