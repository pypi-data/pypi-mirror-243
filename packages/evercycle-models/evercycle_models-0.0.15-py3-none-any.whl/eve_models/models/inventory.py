from django.db import models
from models.audit import Audit


class Inventory(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    make = models.CharField()
    model = models.CharField()
    serial_number = models.CharField(blank=True, null=True)
    memory_size = models.CharField()
    carrier = models.CharField()
    reference = models.CharField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    request = models.ForeignKey('Request', models.DO_NOTHING)
    received = models.BooleanField()
    received_date = models.DateTimeField(blank=True, null=True)
    counted = models.BooleanField()
    device_type = models.CharField()
    imported = models.BooleanField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'inventory'
