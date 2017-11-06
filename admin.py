from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord

class DataMasterAdmin(admin.ModelAdmin):
    list_display = ('master_code','title' )
    fields = ('master_code','title','img_url', 'describe', 'tel','master_uuid',)

class QrLabelAdmin(admin.ModelAdmin):
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','data_master')

class ScanRecordAdmin(admin.ModelAdmin):
    list_display = ('ip','city','scan_date' )
    fields = ('qr_label','ip','json', 'city', )

admin.site.register(DataMaster,DataMasterAdmin)
admin.site.register(QrLabel,QrLabelAdmin)
admin.site.register(ScanRecord,ScanRecordAdmin)

