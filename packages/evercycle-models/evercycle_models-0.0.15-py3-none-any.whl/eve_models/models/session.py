from django.db import models

class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    session_id = models.CharField()
    customer_id = models.CharField()
    amount_subtotal = models.IntegerField()
    amount_total = models.IntegerField()
    payment_intent_id = models.CharField()
    payment_status = models.CharField()

    class Meta:
        managed = False
        db_table = 'session'
