from django.db import models
from eve_models.models import Organization


class Workflow(models.Model):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, models.CASCADE)
