from django.db import models


class Finaldata(models.Model):
    rec_date = models.DateField(primary_key=True)
    pm25 = models.FloatField(blank=True, null=True)
    avg_temp = models.FloatField(blank=True, null=True)
    station = models.IntegerField(blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    org_name = models.CharField(max_length=255, blank=True, null=True)
    season = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'finaldata'