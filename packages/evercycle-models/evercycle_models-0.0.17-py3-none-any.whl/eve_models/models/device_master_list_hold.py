from django.db import models
from .device_list_type import DeviceListType

class DeviceMasterListHold(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    composite_name = models.CharField(max_length=50)
    evercycle_id = models.CharField(max_length=50)
    device_list_type = models.ForeignKey(DeviceListType, models.DO_NOTHING)
    make = models.CharField(max_length=50)
    model_type = models.CharField(max_length=50)
    model_sub = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)
    storage_type = models.CharField(max_length=50)
    storage_amount = models.CharField(max_length=50)
    cpu_brand = models.CharField(max_length=50)
    cpu_model = models.CharField(max_length=50)
    cpu_speed = models.CharField(max_length=50)
    ram_type = models.CharField(max_length=50)
    ram_amount = models.CharField(max_length=50)
    wireless_type = models.CharField(max_length=50)
    wireless_sub = models.CharField(max_length=50)
    asins = models.TextField()  # This field type is a guess.
    keywords_list = models.TextField()  # This field type is a guess.
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'device_master_list_hold'
