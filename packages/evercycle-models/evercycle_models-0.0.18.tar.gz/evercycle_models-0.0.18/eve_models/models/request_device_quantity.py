from django.db import models
from .request import Request

class RequestDeviceQuantity(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    request = models.ForeignKey(Request, models.DO_NOTHING)
    quantity = models.IntegerField()
    device_type = models.ForeignKey('RequestDeviceType', models.DO_NOTHING)
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'request_device_quantity'