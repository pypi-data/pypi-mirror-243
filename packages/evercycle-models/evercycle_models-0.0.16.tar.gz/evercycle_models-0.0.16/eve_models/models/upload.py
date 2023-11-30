from django.db import models
from models.organization import Organization

class Upload(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    csv = models.BinaryField(blank=True, null=True)
    user_id = models.IntegerField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'upload'
