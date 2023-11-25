from django.contrib import admin
from models.Workflow import Workflow
from models.Organization import Organization
from models.Address import Address

# Register your models here.

admin.site.register(Organization)
admin.site.register(Workflow)
admin.site.register(Address)

