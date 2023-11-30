from django.db import models
from .organization import Organization

class OrganizationCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    organization_list = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'organization_collection'
