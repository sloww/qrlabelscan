from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord, LabelRecord, LabelFeedBack
from django import forms
from searchadmin.admin import SelectModelAdmin


class DataMasterAdmin(SelectModelAdmin):
    search_fields = ('title','remark','distributor',)
    list_display = ('master_code','title','remark', 'distributor', )
    fields = ('master_code','title_show','title','img_show',
        'img_url', 'scan_show','describe', 'tel','master_uuid',
        'remark', 'distributor', 'redirect_url','redirect_on',
        'feedback_show',
        )

#class QrLabelAdmin(admin.ModelAdmin):
class QrLabelAdmin(SelectModelAdmin):
    search_fields = ('qrcode',)
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','label_code','data_master',)

class LabelFeedBackAdmin(SelectModelAdmin):
    search_fields = ('feed_back_date','handled',)
    list_display =( 'feed_back_date','feed_back', 'handled' )
    fields  = ('feed_back','uploud_img_url','handled', )


class ScanRecordAdmin(admin.ModelAdmin):
    search_fields = ('city',)
    list_display = ('ip','city','scan_date' )
    fields =  ('ip','city', )

class LabelRecordAdmin(SelectModelAdmin):
    search_fields = ('master_code',)
    list_display = ('master_code','label_code', )
    fields = ('master_code','label_code', )

admin.site.register(DataMaster,DataMasterAdmin)
admin.site.register(QrLabel,QrLabelAdmin)
admin.site.register(ScanRecord,ScanRecordAdmin)
admin.site.register(LabelRecord,LabelRecordAdmin)
admin.site.register(LabelFeedBack,LabelFeedBackAdmin)

