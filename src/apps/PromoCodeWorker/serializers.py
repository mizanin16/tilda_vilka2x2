from rest_framework import serializers

from .models import Promocode


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ['code']
