from django.db import models

class BoxNotification(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracked_box = models.ForeignKey('TrackedBox', models.DO_NOTHING)
    notification_type = models.TextField()  # This field type is a guess.
    email = models.CharField()

    class Meta:
        managed = False
        db_table = 'box_notification'
