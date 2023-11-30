from django.db import models

class Integrations(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    oauth_redirect_url = models.CharField()
    metadata = models.CharField()
    description = models.CharField()
    logo = models.CharField()

    class Meta:
        managed = False
        db_table = 'integrations'

