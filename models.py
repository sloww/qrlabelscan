from django.db import models

# Create your models here.

class Qr(models.Model):
    company_name = models.CharField(max_length=200)
    qrcode = models.CharField(max_length=200)
    scan_times = models.IntegerField(default=0)


class Scan(models.Model):
    qr = models.ForeignKey(Qr, on_delete=models.CASCADE)
    scan_date = models.DateTimeField('date scaned')

class DataMaster(models.Model):
    title = models.CharField(max_length=200)
    master_code = models.CharField(max_length=200,db_index=True,unique=True,null=False)
    describe = models.CharField(max_length=900)
    tel = models.CharField(max_length=200)

    def __str__(self):
        return "%s ( %s )" % (self.master_code,self.title)


class QrLabel(models.Model):
    data_master = models.ForeignKey(DataMaster, on_delete=models.CASCADE)
    qrcode = models.CharField(max_length=200,db_index=True,unique=True,null=False)

    def __str__(self):
        return "%s ( %s )" % (self.qrcode, self.data_master.master_code)
