from django.db import models

# Create your models here.

class Qr(models.Model):
    company_name = models.CharField(max_length=200)
    qrcode = models.CharField(max_length=200)
    scan_times = models.IntegerField(default=0)


class Scan(models.Model):
    qr = models.ForeignKey(Qr, on_delete=models.CASCADE)
    scan_date = models.DateTimeField('date scaned')
