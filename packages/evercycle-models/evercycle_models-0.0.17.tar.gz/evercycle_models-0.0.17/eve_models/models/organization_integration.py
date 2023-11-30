from django.db import models
from .organization import Organization
from .integrations import Integrations

class OrganizationIntegration(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    integrations = models.ForeignKey(Integrations, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organization_integration'
