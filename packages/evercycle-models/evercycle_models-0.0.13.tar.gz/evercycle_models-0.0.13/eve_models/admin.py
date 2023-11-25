from django.contrib import admin
from eve_models.models.Workflow import Workflow
from eve_models.models.Organization import Organization
from eve_models.models.Address import Address

# Register your models here.

admin.site.register(Organization)
admin.site.register(Workflow)
admin.site.register(Address)

