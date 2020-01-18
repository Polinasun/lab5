from django.db import models
from uuid import uuid4

class Menu(models.Model):
    menu_category = (
        ('0', 'breakfast'),
        ('1', 'lunch'),
        ('2', 'dinner'),
    )

    menu_category = models.CharField(max_length = 1, choices = menu_category)
    number_room=models.IntegerField()
    room_id=models.UUIDField(default = uuid4)
    #guest = models.UUIDField(default = uuid4)
    uuid = models.UUIDField(primary_key = True, default = uuid4)



    def __str__(self):
        return self.title
