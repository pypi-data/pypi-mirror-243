from django.db import models
from models.organization import Organization
from models.program import Program

class Settings(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    user_id = models.IntegerField()
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    active_program = models.ForeignKey(Program, models.DO_NOTHING)
    page = models.TextField()  # This field type is a guess.
    request = models.TextField()  # This field type is a guess.
    dashboard = models.TextField()  # This field type is a guess.
    updated_at = models.DateTimeField()
    updated_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'settings'
