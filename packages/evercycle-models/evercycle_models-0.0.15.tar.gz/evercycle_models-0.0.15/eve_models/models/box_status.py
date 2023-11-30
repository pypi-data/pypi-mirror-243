from django.db import models

class BoxStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()

    class Meta:
        managed = False
        db_table = 'box_status'
