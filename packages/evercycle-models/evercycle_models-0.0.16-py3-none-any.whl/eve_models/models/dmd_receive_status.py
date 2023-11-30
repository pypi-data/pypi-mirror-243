from django.db import models

class DmdReceiveStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dmd_receive_status'
