from django.db import models
from .asset import Asset
from .asset_damage_type import AssetDamageType


class AssetHistory(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    asset = models.ForeignKey(Asset, models.DO_NOTHING)
    updated_at = models.DateTimeField()
    user_id = models.IntegerField()
    asset_status_change_from = models.ForeignKey('AssetStatus', models.DO_NOTHING)
    asset_status_change_to = models.ForeignKey('AssetStatus', models.DO_NOTHING, related_name='assethistory_asset_status_change_to_set')
    asset_damage_type = models.ForeignKey(AssetDamageType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'asset_history'
