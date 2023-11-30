from django.db import models

class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    asset_status = models.ForeignKey('AssetStatus', models.DO_NOTHING)
    asset_type = models.ForeignKey('AssetType', models.DO_NOTHING)
    year = models.CharField(blank=True, null=True, max_length=100)
    make = models.CharField(blank=True, null=True, max_length=100)
    model = models.CharField(blank=True, null=True, max_length=100)
    serial_number = models.CharField(blank=True, null=True, max_length=100)
    asset_damage_type = models.ForeignKey('AssetDamageType', models.DO_NOTHING)
    damage_description = models.CharField(blank=True, null=True, max_length=100)
    carrier = models.CharField(blank=True, null=True, max_length=100)
    cpu = models.CharField(blank=True, null=True, max_length=100)
    ram = models.CharField(blank=True, null=True, max_length=100)
    screen = models.CharField(blank=True, null=True, max_length=100)
    purchase_date = models.DateField(blank=True, null=True)
    asset_reference = models.CharField(blank=True, null=True, max_length=100)
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)
    asset_user_first_name = models.CharField(blank=True, null=True, max_length=100)
    asset_user_last_name = models.CharField(blank=True, null=True, max_length=100)
    asset_user_address = models.CharField(blank=True, null=True, max_length=100)
    asset_user_city = models.CharField(blank=True, null=True, max_length=100)
    asset_user_state = models.CharField(blank=True, null=True, max_length=100)
    asset_user_postal_code = models.CharField(blank=True, null=True, max_length=100)
    asset_user_country = models.CharField(blank=True, null=True, max_length=100)
    request = models.ForeignKey('Request', models.DO_NOTHING)
    archived = models.BooleanField()
    device_master_list = models.ForeignKey('DeviceMasterList', models.DO_NOTHING)
    request_uid = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'asset'
