from django.db import models
from models.tracking import Tracking
from models.shipping_status import ShippingStatus
from models.shipping_status_easypost import ShippingStatusEasypost

class TrackingStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracking = models.ForeignKey(Tracking, models.DO_NOTHING)
    checkpoint_order = models.IntegerField()
    detailed_status = models.CharField()
    city = models.CharField()
    state = models.CharField()
    postal_code = models.CharField()
    country = models.CharField()
    status_date = models.DateTimeField()
    shipping_status = models.ForeignKey(ShippingStatus, models.DO_NOTHING)
    shipping_status_easypost = models.ForeignKey(ShippingStatusEasypost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tracking_status'
