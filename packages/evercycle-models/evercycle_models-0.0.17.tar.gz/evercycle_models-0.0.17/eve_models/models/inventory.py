from django.db import models
from .audit import Audit


class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(blank=True, null=True)
    memory_size = models.CharField(max_length=50)
    carrier = models.CharField(max_length=50)
    reference = models.CharField(max_length=50)
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    request = models.ForeignKey('Request', models.DO_NOTHING)
    received = models.BooleanField()
    received_date = models.DateTimeField(blank=True, null=True)
    counted = models.BooleanField()
    device_type = models.CharField(max_length=50)
    imported = models.BooleanField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'inventory'
