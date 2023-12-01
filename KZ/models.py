from django.db import models


class Graphic(models.Model):
    cur_chartType = models.CharField(max_length=20)
    cur_dataTable = models.CharField(max_length=200)
    more = models.CharField(max_length=100)
    cur_title = models.CharField(max_length=100)


class Object(models.Model):
    square = models.IntegerField()
    address = models.CharField(max_length=100)
    email_address = models.CharField(max_length=30)
    object_type = models.CharField(max_length=15)
