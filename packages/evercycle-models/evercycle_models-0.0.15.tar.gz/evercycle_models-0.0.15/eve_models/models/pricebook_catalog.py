from django.db import models
from models.device_master_list import DeviceMasterList

class PricebookCatalog(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    device_master_list = models.ForeignKey(DeviceMasterList, models.DO_NOTHING)
    sp_pricebook = models.ForeignKey('SpPricebook', models.DO_NOTHING)
    test = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'pricebook_catalog'
