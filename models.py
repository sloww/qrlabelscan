#coding:utf-8   

from django.db import models
import uuid

class DataMaster(models.Model):
    title = models.CharField(max_length=200)
    img_url = models.URLField(max_length=200)
    master_code = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        )
    describe = models.CharField(max_length=900)
    tel = models.CharField(max_length=200)

    def __str__(self):
        return "%s ( %s )" % (self.master_code,self.title)

class QrLabel(models.Model):
    data_master = models.ForeignKey(DataMaster,
        on_delete=models.CASCADE,
        )
    qrcode = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        )

    def __str__(self):
        return "%s ( %s )" % (self.qrcode, self.data_master.master_code)

    def scaned(self,ip):
        sr =ScanRecord(qr_label=self, ip=ip,) 
        print(sr.ip)
        sr.save()

    def scaned_time(self):
        return  ScanRecord.objects.filter(qr_label=self).count()

    def get_first_scan(self):
        return ScanRecord.objects.filter(qr_label=self).order_by('scan_date').first()

class ScanRecord(models.Model):
    qr_label = models.ForeignKey(QrLabel, on_delete=models.CASCADE)
    ip=models.GenericIPAddressField()
    scan_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return "%s ( %s )" % (self.scan_date, self.qr_label.qrcode)
