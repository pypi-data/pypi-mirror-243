from django.db import models
from models.organization import Organization

class Quote(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    device_object = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'quote'