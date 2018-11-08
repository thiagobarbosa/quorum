from django.db import models
#import urllib2
import json
from django_pandas.managers import DataFrameManager



class Debito(models.Model):
#    req = urllib2.Request("http://app-sisgvconsulta-prd.azurewebsites.net/ws/ws2.asmx/ObterDebitoVereadorJSON?ano=2018&mes=01")
    id_ver = models.IntegerField()
    name = models.CharField(max_length=100)
    objects = DataFrameManager()

#    print(req)
