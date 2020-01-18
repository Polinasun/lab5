from django.db import models
from uuid import uuid4

class Rooms(models.Model):
    rooms_type = (
        ('0', 'standard'),
        ('1', 'Apartmant'),
        ('2', 'Business'),
        ('3', 'De luxe'),
        ('4', 'President'),
    )

    category = models.CharField(max_length = 1, choices = rooms_type)
    number_room=models.IntegerField()
    bed1 = models.UUIDField(default = uuid4)
    uuid = models.UUIDField(primary_key = True, default = uuid4)



    def __str__(self):
        return self.title

class CustomToken(models.Model):
    token = models.CharField(verbose_name = 'Token', max_length = 40)
    created = models.DateTimeField(verbose_name = 'Creation Date', auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()

        return super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token