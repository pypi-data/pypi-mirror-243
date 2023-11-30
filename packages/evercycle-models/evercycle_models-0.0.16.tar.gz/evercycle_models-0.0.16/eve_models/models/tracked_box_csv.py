from django.db import models
from models.organization import Organization

class TrackedBoxCsv(models.Model):
    id = models.IntegerField(primary_key=True)
    request_uid = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    note = models.CharField(max_length=50)
    status_date = models.DateField(blank=True, null=True)
    program = models.CharField(max_length=50)
    organization = models.CharField(max_length=50)
    outbound_tracking = models.CharField(max_length=50)
    return_tracking = models.CharField(max_length=50)
    request_reference = models.CharField(max_length=50)
    package = models.CharField(max_length=50)
    date_requested = models.DateField(blank=True, null=True)
    package_status = models.CharField(max_length=50)
    carrier_status_date = models.DateField(blank=True, null=True)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    contact_address = models.CharField(max_length=50)
    serials = models.TextField()  # This field type is a guess.
    device_types = models.TextField()  # This field type is a guess.
    organization_0 = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization_id')  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'tracked_box_csv'