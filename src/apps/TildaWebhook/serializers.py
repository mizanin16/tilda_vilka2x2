from rest_framework import serializers
from .models import Delivery
from .models import ListAuthUsers


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['address', 'name', 'phone']


class ListAuthUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListAuthUsers
        fields = ['name', 'email', 'phone']
