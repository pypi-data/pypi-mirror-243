from django.db import models

class CountryCodes(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=50)
    alpha_2_code = models.CharField(max_length=50)
    alpha_3_code = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'country_codes'
