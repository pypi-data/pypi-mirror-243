from django.db import models
from models.organization import Organization

class TrackedBoxCsv(models.Model):
    id = models.IntegerField(primary_key=True)
    request_uid = models.CharField()
    status = models.CharField()
    note = models.CharField()
    status_date = models.DateField(blank=True, null=True)
    program = models.CharField()
    organization = models.CharField()
    outbound_tracking = models.CharField()
    return_tracking = models.CharField()
    request_reference = models.CharField()
    package = models.CharField()
    date_requested = models.DateField(blank=True, null=True)
    package_status = models.CharField()
    carrier_status_date = models.DateField(blank=True, null=True)
    contact_first_name = models.CharField()
    contact_last_name = models.CharField()
    contact_address = models.CharField()
    serials = models.TextField()  # This field type is a guess.
    device_types = models.TextField()  # This field type is a guess.
    organization_0 = models.ForeignKey(Organization, models.DO_NOTHING, db_column='organization_id')  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'tracked_box_csv'