from datetime import datetime

from django.db import models
from django.utils import datetime_safe


# Create your models here.
class Usero(models.Model):
    phone = models.IntegerField(max_length=11)
    mailo = models.TextField(max_length=45)
    passwordo = models.TextField(max_length=45)


class City(models.Model):
    FullNameCity = models.TextField(max_length=45)


class Street(models.Model):
    FullStreet = models.TextField(max_length=45)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)


class Parking(models.Model):
    quanityPlaces = models.IntegerField(max_length=3)
    Street_id = models.ForeignKey(Street, on_delete=models.CASCADE)


class Orders(models.Model):
    timeStart = models.TextField()
    occupiedPlace = models.IntegerField(max_length=3)
    statuso = models.BooleanField()
    usero_idusero = models.ForeignKey(Usero, on_delete=models.CASCADE)
    Parking_id = models.ForeignKey(Parking, on_delete=models.CASCADE)


class Admins(models.Model):
    adm_nick = models.TextField(max_length=45)
    adm_passw = models.TextField(max_length=45)

class priceo(models.Model):
    price = models.IntegerField()