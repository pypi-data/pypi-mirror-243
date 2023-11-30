from django.db import models

class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    asset_status = models.ForeignKey('AssetStatus', models.DO_NOTHING)
    asset_type = models.ForeignKey('AssetType', models.DO_NOTHING)
    year = models.CharField(blank=True, null=True)
    make = models.CharField(blank=True, null=True)
    model = models.CharField(blank=True, null=True)
    serial_number = models.CharField(blank=True, null=True)
    asset_damage_type = models.ForeignKey('AssetDamageType', models.DO_NOTHING)
    damage_description = models.CharField(blank=True, null=True)
    carrier = models.CharField(blank=True, null=True)
    cpu = models.CharField(blank=True, null=True)
    ram = models.CharField(blank=True, null=True)
    screen = models.CharField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    asset_reference = models.CharField(blank=True, null=True)
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)
    asset_user_first_name = models.CharField(blank=True, null=True)
    asset_user_last_name = models.CharField(blank=True, null=True)
    asset_user_address = models.CharField(blank=True, null=True)
    asset_user_city = models.CharField(blank=True, null=True)
    asset_user_state = models.CharField(blank=True, null=True)
    asset_user_postal_code = models.CharField(blank=True, null=True)
    asset_user_country = models.CharField(blank=True, null=True)
    request = models.ForeignKey('Request', models.DO_NOTHING)
    archived = models.BooleanField()
    device_master_list = models.ForeignKey('DeviceMasterList', models.DO_NOTHING)
    request_uid = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'asset'
