from django.db import models
from models.organization import Organization
from models.processor import Processor
from models.carrier import Carrier

class Program(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    program_name = models.CharField(max_length=50)
    program_description = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    warehouse = models.ForeignKey(Processor, models.DO_NOTHING)
    program_type = models.ForeignKey('ProgramType', models.DO_NOTHING)
    created_by = models.IntegerField()
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.IntegerField()
    three_tier_grade = models.BooleanField()
    gradescaletype = models.CharField(max_length=50)
    purchaser = models.ForeignKey('Purchaser', models.DO_NOTHING)
    notify_locks = models.BooleanField()
    disable_email_notification = models.BooleanField()
    bill_to_my_other_account = models.CharField(max_length=50)
    outbound_service_level = models.TextField()  # This field type is a guess.
    return_service_level = models.TextField()  # This field type is a guess.
    aftership_slug = models.CharField(max_length=50)
    service = models.TextField()  # This field type is a guess.
    carrier = models.ForeignKey(Carrier, models.DO_NOTHING)
    test = models.BooleanField()
    device_location_type = models.TextField()  # This field type is a guess.
    device_location_type_conus_choice = models.TextField()  # This field type is a guess.
    workflow_poc = models.CharField(max_length=50)
    workflow_poc_email = models.CharField(max_length=50)
    service_provider = models.ForeignKey('ServiceProvider', models.DO_NOTHING)
    workflow_status = models.TextField()  # This field type is a guess.
    device_sample = models.CharField(max_length=50)
    frequency_type = models.TextField()  # This field type is a guess.
    frequency = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'program'
