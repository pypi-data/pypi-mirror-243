from django.db import models


class Address(models.Model):
    name = models.CharField(max_length=50)
