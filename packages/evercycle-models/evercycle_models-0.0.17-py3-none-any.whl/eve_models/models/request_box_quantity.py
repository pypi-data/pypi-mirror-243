from django.db import models
from .package_type import PackageType
from .request import Request

class RequestBoxQuantity(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    package_type = models.ForeignKey(PackageType, models.DO_NOTHING)
    request = models.ForeignKey(Request, models.DO_NOTHING)
    quantity = models.IntegerField()
    sleeve_count = models.IntegerField()
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'request_box_quantity'