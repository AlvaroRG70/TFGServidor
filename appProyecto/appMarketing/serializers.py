from rest_framework import serializers
from .models import *
from datetime import date


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'
        
        
        