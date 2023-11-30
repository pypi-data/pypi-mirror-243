from django.contrib import admin
from eve_models.models.address import Address
from eve_models.models.asset import Asset

# Register your models here.

admin.site.register(Address)
admin.site.register(Asset)
