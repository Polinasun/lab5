from rest_framework import serializers
from .models import Menu

class menu_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
