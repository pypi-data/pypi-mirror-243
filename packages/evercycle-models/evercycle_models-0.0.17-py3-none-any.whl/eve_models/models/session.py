from django.db import models

class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    session_id = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=50)
    amount_subtotal = models.IntegerField()
    amount_total = models.IntegerField()
    payment_intent_id = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'session'
