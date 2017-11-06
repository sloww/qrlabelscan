from django.contrib import admin

from .models import DataMaster,QrLabel

class DataMasterAdmin(admin.ModelAdmin):
    list_display = ('master_code','title' )
    fields = ('master_code','title','img_url', 'describe', 'tel','master_uuid',)

class QrLabelAdmin(admin.ModelAdmin):
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','data_master')

admin.site.register(DataMaster,DataMasterAdmin)
admin.site.register(QrLabel,QrLabelAdmin)

