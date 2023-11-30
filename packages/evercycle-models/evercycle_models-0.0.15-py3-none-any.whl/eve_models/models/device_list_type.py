from django.db import models

class DeviceListType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'device_list_type'
