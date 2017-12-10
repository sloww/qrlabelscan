from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord, LabelRecord, LabelFeedBack
from django import forms
from searchadmin.admin import SelectModelAdmin

#新加入的包
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
from django.contrib.auth import get_user_model
User = get_user_model()



#此处更改，相当于创了另一个页面
class MyAdminSite(AdminSite):
    #网站标签页标题
    site_title = ugettext_lazy('二维码分发平台')
    #网站标题
    site_header = ugettext_lazy('二维码分发平台')

admin_site = MyAdminSite()


class DataMasterAdmin(SelectModelAdmin):
    search_fields = ('title','remark','distributor',)
    list_display = ('master_code','title','remark', 'distributor', )
    fields = ('master_code','title_show','title','img_show',
        'img_url', 'scan_show','describe','describe_show', 'tel','company','master_uuid',
        'remark', 'distributor', 'redirect_url','redirect_on',
        'feedback_show',
        'sales_on',
        )

#class QrLabelAdmin(admin.ModelAdmin):
class QrLabelAdmin(SelectModelAdmin):
    search_fields = ('qrcode',)
    list_display = ('qrcode','data_master' )
    fields = ('label_uuid','qrcode','label_code','data_master',)

class LabelFeedBackAdmin(SelectModelAdmin):
    search_fields = ('date_time','handled',)
    list_display =( 'date_time','feed_back', 'handled' )
    fields  = ('feed_back','upload_img_url','handled', )


class ScanRecordAdmin(admin.ModelAdmin):
    search_fields = ('city',)
    list_display = ('ip','city','scan_date' )
    fields =  ('ip','city', )

class LabelRecordAdmin(SelectModelAdmin):
    search_fields = ('master_code',)
    list_display = ('master_code','label_code', )
    fields = ('master_code','label_code', )

admin_site.register(DataMaster,DataMasterAdmin)
admin_site.register(QrLabel,QrLabelAdmin)
admin_site.register(ScanRecord,ScanRecordAdmin)
admin_site.register(LabelRecord,LabelRecordAdmin)
admin_site.register(LabelFeedBack,LabelFeedBackAdmin)
admin_site.register(User)

