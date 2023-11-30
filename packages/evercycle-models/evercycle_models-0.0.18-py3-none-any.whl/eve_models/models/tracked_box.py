from django.db import models
from .request import Request
from .package_type import PackageType
from .box_status import BoxStatus


class TrackedBox(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    package_type = models.ForeignKey(PackageType, models.DO_NOTHING)
    outgoing_tracking = models.ForeignKey('Tracking', models.DO_NOTHING)
    return_tracking = models.ForeignKey('Tracking', models.DO_NOTHING, related_name='trackedbox_return_tracking_set')
    request = models.ForeignKey(Request, models.DO_NOTHING)
    box_status = models.ForeignKey(BoxStatus, models.DO_NOTHING)
    status_date = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=50)
    error = models.CharField(max_length=50)
    sleeve_count = models.IntegerField()
    request_uid = models.CharField(max_length=50)
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tracked_box'
