from django.db import models

class Tracking(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracking_number = models.CharField(max_length=50)
    last_checkpoint = models.IntegerField()
    updated_at = models.DateTimeField()
    retrack_count = models.IntegerField()
    last_retrack_date = models.DateTimeField(blank=True, null=True)
    label = models.CharField(max_length=50)
    last_print_date = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField()
    archived = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tracking'
