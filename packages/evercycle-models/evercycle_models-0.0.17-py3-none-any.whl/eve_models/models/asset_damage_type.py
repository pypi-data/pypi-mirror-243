from django.db import models

class AssetDamageType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    damage_type = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'asset_damage_type'
