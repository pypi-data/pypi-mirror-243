from django.db import models
from models.dmd_receive_status import DmdReceiveStatus

class DmdReceivingJournal(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracked_box = models.ForeignKey('TrackedBox', models.DO_NOTHING)
    dmd_receive_status = models.ForeignKey(DmdReceiveStatus, models.DO_NOTHING)
    note = models.CharField(max_length=50)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dmd_receiving_journal'
