from django.db import models

class ReplacedTracking(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracked_box_id = models.IntegerField()
    outbound_tracking = models.ForeignKey('Tracking', models.DO_NOTHING)
    return_tracking = models.ForeignKey('Tracking', models.DO_NOTHING, related_name='replacedtracking_return_tracking_set')

    class Meta:
        managed = False
        db_table = 'replaced_tracking'
