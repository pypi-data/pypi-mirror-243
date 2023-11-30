from django.db import models
from .organization import Organization

class ServiceProvider(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    logo = models.BinaryField(blank=True, null=True)
    description = models.CharField(max_length=50)
    headquarters_address = models.CharField(max_length=50)
    warehouse_address = models.CharField(max_length=50)
    device_specialization = models.CharField(max_length=50)
    industry_specialization = models.CharField(max_length=50)
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    certifications = models.TextField()  # This field type is a guess.
    services = models.TextField()  # This field type is a guess.
    report_services = models.TextField()  # This field type is a guess.
    warehouse_security = models.TextField()  # This field type is a guess.
    audit_report_sla = models.TextField()  # This field type is a guess.
    sample_audit_report = models.BinaryField(blank=True, null=True)
    device_audit_pictures = models.TextField()  # This field type is a guess.
    data_erasure_id = models.TextField()  # This field type is a guess.
    payment_terms = models.TextField()  # This field type is a guess.
    payment_methods = models.TextField()  # This field type is a guess.
    processor_id = models.TextField()  # This field type is a guess.
    service_provider_workflow_email = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'service_provider'