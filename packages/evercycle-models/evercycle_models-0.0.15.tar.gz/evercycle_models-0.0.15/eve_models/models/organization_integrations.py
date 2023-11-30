from django.db import models
from models.organization import Organization
from models.integrations import Integrations

class OrganizationIntegrations(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    integrations = models.ForeignKey(Integrations, models.DO_NOTHING)
    metadata = models.CharField()
    archived = models.BooleanField()
    foreign_id = models.CharField()

    class Meta:
        managed = False
        db_table = 'organization_integrations'
