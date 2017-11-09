from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord, LabelRecord
from django import forms


class DataMasterAdmin(admin.ModelAdmin):
    list_display = ('master_code','title','remark', 'distributor', )
    fields = ('master_code','title','img_url', 'describe', 'tel','master_uuid','remark', 'distributor', )


class QrLabelAdmin(admin.ModelAdmin):
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','label_code','data_master')

class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('ip','city','scan_date' )
    fields = ('qr_label','ip','json', 'city', )

class LabelRecordAdmin(admin.ModelAdmin):
    list_display = ('master_code','label_code', )
    fields = ('master_code','label_code', )

admin.site.register(DataMaster,DataMasterAdmin)
admin.site.register(QrLabel,QrLabelAdmin)
admin.site.register(ScanRecord,ScanRecordAdmin)
admin.site.register(LabelRecord,LabelRecordAdmin)

