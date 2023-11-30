from django.db import models
from models.device_list_type import DeviceListType

class WipDeviceMasterList(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    composite_name = models.CharField()
    evercycle_id = models.CharField()
    device_list_type = models.ForeignKey(DeviceListType, models.DO_NOTHING)
    make = models.CharField()
    model_type = models.CharField()
    model_sub = models.CharField()
    year = models.CharField()
    screen_size = models.CharField()
    dimensions = models.CharField()
    storage_type = models.CharField()
    storage_amount = models.CharField()
    cpu_brand = models.CharField()
    cpu_model = models.CharField()
    cpu_speed = models.CharField()
    ram_type = models.CharField()
    ram_amount = models.CharField()
    wireless_type = models.CharField()
    wireless_sub = models.CharField()
    asins = models.TextField()  # This field type is a guess.
    keywords_list = models.TextField()  # This field type is a guess.
    image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wip_device_master_list'
