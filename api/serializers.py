from rest_framework import serializers
from .models import MainModel, Boost

class MainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainModel
        fields = '__all__'

class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['id', 'power', 'price', 'level', 'boost_type']