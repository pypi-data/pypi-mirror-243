from django.contrib import admin
from eve_models.models.address import Address
from eve_models.models.asset import Asset
from eve_models.models.asset_damage_type import AssetDamageType
from eve_models.models.organization import Organization

# Register your models here.

admin.site.register(Address)
admin.site.register(Asset)
admin.site.register(Organization)
admin.site.register(AssetDamageType)
