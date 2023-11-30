from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=50)


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)