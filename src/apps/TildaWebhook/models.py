from django.db import models
from django.utils import timezone


class ListAuthUsers(models.Model):
    id_user = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'ID: {self.id_user}, Name: {self.name}, Email: {self.email}, Phone: {self.phone}'


class Delivery(models.Model):
    id_delivery = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, verbose_name='Адрес_доставки')
    name = models.CharField(max_length=100, verbose_name='Name')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    datetime_order = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
