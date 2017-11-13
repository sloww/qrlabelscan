from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord, LabelRecord
from django import forms
from searchadmin.admin import SelectModelAdmin


class DataMasterAdmin(SelectModelAdmin):
    search_fields = ('title','remark','distributor',)
    list_display = ('master_code','title','remark', 'distributor', )
    fields = ('master_code','title_show','title','img_show','img_url', 'scan_show','describe', 'tel','master_uuid','remark', 'distributor', )


#class QrLabelAdmin(admin.ModelAdmin):
class QrLabelAdmin(SelectModelAdmin):
    search_fields = ('qrcode',)
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','label_code','data_master')

class ScanRecordAdmin(SelectModelAdmin):
    search_fields = ('city',)
    list_display = ('ip','city','scan_date' )

class LabelRecordAdmin(SelectModelAdmin):
    search_fields = ('master_code',)
    list_display = ('master_code','label_code', )
    fields = ('master_code','label_code', )

admin.site.register(DataMaster,DataMasterAdmin)
admin.site.register(QrLabel,QrLabelAdmin)
admin.site.register(ScanRecord,ScanRecordAdmin)
admin.site.register(LabelRecord,LabelRecordAdmin)

