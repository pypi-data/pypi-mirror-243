from django.db import models
from .processor import Processor

class RequestDeviceType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    device = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    processor = models.ForeignKey(Processor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'request_device_type'
