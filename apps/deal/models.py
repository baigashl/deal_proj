import datetime

from django.db import models


class Gem(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)


class Customer(models.Model):
    username = models.CharField(max_length=255, null=False, blank=False)
    item = models.CharField(max_length=255, null=False, blank=False)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.CharField(max_length=255, null=False, blank=False)


class Deal(models.Model):
    username = models.CharField(max_length=255, unique=True, null=False, blank=False)
    spent_money = models.IntegerField()
    gems = models.ManyToManyField(Gem)


def upload_file(instance, filename):
    return 'files/{filename}'.format(filename=filename)


class File(models.Model):
    file = models.FileField(upload_to=upload_file)
    time_stamp = models.DateTimeField(default=datetime.datetime.now)




