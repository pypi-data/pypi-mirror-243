from django.db import models

class Role(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    description = models.CharField()

    class Meta:
        managed = False
        db_table = 'role'
