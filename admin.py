from django.contrib import admin

from .models import DataMaster,QrLabel, ScanRecord, LabelRecord, LabelFeedBack,DMP
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

#此处更改，相当于创了另一个页面
class QrAdminSite(AdminSite):
    #网站标签页标题
    site_title = ugettext_lazy('智码分发平台')
    #网站标题
    site_header = ugettext_lazy('智码分发平台')

qr_admin = QrAdminSite()



class DataMasterAdmin(SelectModelAdmin):
    search_fields = ('title','remark','distributor',)
    list_display = ('master_code','title','remark', 'distributor', 'fix','fd_url','grl_url','label_list')
    fields = ('master_uuid',
        'master_code',
        ('title','title_show',),
        ('img_url','img_show',),
        'scan_show',
        ('describe','describe_show'),
        'tel','company',
        'remark', 'distributor', 
        'redirect_url_wx','redirect_url_jd','redirect_url_tb','redirect_url','redirect_on',
        'feedback_show',
        'sales_on',
        'template',
        'fd_url',
        'grl_url',
        'has_fix',
        'label_list2',
        )
    readonly_fields = ('master_uuid','fd_url','grl_url','label_list2','master_code',)

class DMPAdmin(SelectModelAdmin):
    search_fields = ('title','remark','distributor',)
    list_display = ('master_code','title','remark', 'distributor','grl_url', 'fd_url')
    fields = ('master_uuid',
        'master_code',
        ('title','title_show',),
        ('img_url','img_show',),
        'scan_show',
        ('describe','describe_show'),
        'tel','company',
        'remark', 'distributor', 
        ('redirect_url_wx','redirect_url_jd','redirect_url_tb','redirect_url','redirect_on'),
        'feedback_show',
        'sales_on',
        'template',
        'fd_url',
        'grl_url',
        )
    readonly_fields = ('master_uuid','fd_url','grl_url')


#class QrLabelAdmin(admin.ModelAdmin):
class QrLabelAdmin(SelectModelAdmin):
    search_fields = ('qrcode','master_code',)
    list_display = ('qrcode','data_master','remark','format_url' ,'qr_url')
    fields = ('label_uuid','qrcode','label_code','master_code','data_master','remark','mark_date','equip_no','equip_img_url','format_url','qr_url')
    readonly_fields=('label_uuid','format_url','qr_url','master_code',)

class LabelFeedBackAdmin(SelectModelAdmin):
    search_fields = ('date_time','handled',)
    list_display =( 'date_time','feed_back', 'handled' )
    fields  = ('feed_back','upload_img_url','handled', )


class ScanRecordAdmin(SelectModelAdmin):
    search_fields = ('city','ip')
    list_display = ('ip','city','date','qrcode','label_remark','master_code','labels_remark')
    readonly_fields = ('ip','date','qrcode','label_remark','master_code','labels_remark')
    fields = ('ip','date','qrcode','label_remark','master_code','labels_remark')

class LabelRecordAdmin(SelectModelAdmin):
    search_fields = ('master_code',)
    list_display = ('master_code','label_code', )
    fields = ('master_code','label_code', )

admin_site.register(DataMaster,DataMasterAdmin)
admin_site.register(DMP,DMPAdmin)
admin_site.register(QrLabel,QrLabelAdmin)
admin_site.register(ScanRecord,ScanRecordAdmin)
admin_site.register(LabelRecord,LabelRecordAdmin)
admin_site.register(LabelFeedBack,LabelFeedBackAdmin)
admin_site.register(User)

qr_admin.register(DataMaster,DataMasterAdmin)
qr_admin.register(DMP,DMPAdmin)
qr_admin.register(QrLabel,QrLabelAdmin)
qr_admin.register(ScanRecord,ScanRecordAdmin)
qr_admin.register(LabelRecord,LabelRecordAdmin)
qr_admin.register(LabelFeedBack,LabelFeedBackAdmin)

