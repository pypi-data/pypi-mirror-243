from django.db import models

class IntegrationUser(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    user_id = models.CharField()
    integrations = models.ForeignKey('Integrations', models.DO_NOTHING)
    meta_data = models.CharField()

    class Meta:
        managed = False
        db_table = 'integration_user'
