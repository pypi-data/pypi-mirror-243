from django.db import models

class AssetStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    status = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'asset_status'
