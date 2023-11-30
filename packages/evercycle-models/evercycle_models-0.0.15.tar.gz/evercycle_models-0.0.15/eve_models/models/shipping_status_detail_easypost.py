from django.db import models

class ShippingStatusDetailEasypost(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    status_id = models.IntegerField()
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'shipping_status_detail_easypost'