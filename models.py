#coding:utf-8   

from django.db import models
import uuid
from datetime import datetime
from django.utils.html import format_html
from django.conf import settings

class LabelRecord(models.Model):
    master_code = models.IntegerField(
        verbose_name="管理码编号",
        default=1,
        )
    label_code = models.IntegerField(
        verbose_name="粘贴码序号",
        default=1,
        )

    class Meta():
        verbose_name = "申请记录"
        verbose_name_plural = '0.申请记录'

class DataMaster(models.Model):

    master_uuid =models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="管理码",
        )
    master_code = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="管理码编号",
        )

    title = models.CharField(max_length=200,
        verbose_name="标题",
        )
    title_show = models.BooleanField(default =True,
        verbose_name = '是否显示标题',
        )

    company = models.CharField(max_length=200,
        verbose_name="单位",
        default = "太数智能科技（上海）有限公司",
        )
    remark = models.CharField(max_length=200,
        default="",
        blank = True,
        verbose_name="备注",
        )
    distributor = models.CharField(max_length=200,
        default="",
        blank = True,
        verbose_name="经销商",
        )

    img_url = models.URLField(max_length=200,
        verbose_name="主图地址",
        blank = True,
        )
    redirect_url = models.CharField(max_length=200,
        verbose_name="跳转地址",
        default = "http://tslink.cc"
        )
    redirect_on = models.BooleanField(default = False,
        verbose_name = '是否跳转',
        )
    img_show = models.BooleanField(default = True,
        verbose_name = '是否显示主图',
        )

    describe = models.TextField(max_length=900,
        blank = True,
        default="",
        verbose_name="文字描述",
        )

    scan_show = models.BooleanField(default = True,
        verbose_name = '是否显示扫描结果',
        )

    describe_show = models.BooleanField(
        default = True,
        verbose_name = '是否显示描述信息',
        )
    feedback_show = models.BooleanField(
        default = False,
        verbose_name = '是否开启标签反馈模块',
        )

    tel = models.CharField(
        max_length=200,
        verbose_name="电话",
        )

    template = models.CharField(
        max_length=200,
        verbose_name = "模版名称",
        default = 'v1/qrscan.html', 
        )

    def fd_url(self):
        return  format_html(
            '<a href="/a/{}/feedback/">反馈清单</a>',
            self.master_uuid,
        )


    sales_on = models.BooleanField(
        default = False,
        verbose_name = '售后码',
        )
   
    def __str__(self):
        return "%s ( %s )" % (self.master_code,self.title)

    class Meta():
        verbose_name = "标签组"
        verbose_name_plural = '2.标签组'

    def label_count(self):
        return  QrLabel.objects.filter(data_master=self).count()


class DMP(DataMaster):
     class Meta():
        verbose_name = '标签组模版'
        verbose_name_plural = '1.标签组模版'
        
class QrLabel(models.Model):
    data_master = models.ForeignKey(DataMaster,
        on_delete=models.CASCADE,
        )
    label_uuid =models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="粘贴码",
        )
    label_code = models.CharField(
        max_length=200,
        verbose_name="粘贴码序号",
        )
    remark = models.CharField(
        max_length=200,
        verbose_name="备注",
        default = "-"
        )
    qrcode = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name="粘贴码编号",
        )

    url = models.URLField(
        verbose_name = "URL地址",
        blank = True,
        )
    has_sale = models.BooleanField(
        verbose_name = '售出',
        default = False,
        )

    equip_no = models.CharField(
        max_length=200,
        verbose_name="设备序列号",
        default = ""
        )
    

    equip_img_url = models.URLField(max_length=200,
        verbose_name="图片地址",
        blank = True,
        )

    mark_date = models.DateTimeField(
        verbose_name = '标记时间',
        default=datetime.now(),
        blank=True,
        )

    def __str__(self):
        return "%s ( %s )" % (self.qrcode, self.data_master.master_code)

    def format_url(self):
        return  format_html(
            '<a href="{}">{}</a>',
            self.url,
            self.url,
        )

    class Meta():
        verbose_name = "标签"
        verbose_name_plural = '3.标签'

    def scaned_times(self):
        return  ScanRecord.objects.filter(qr_label=self).count()

    def get_first_scan(self):
        return ScanRecord.objects.filter(qr_label=self).order_by('scan_date').first()

    def save(self, *args, **kwargs):
        self.url = settings.URLPRE+self.label_uuid+'/'
        super(QrLabel, self).save(*args, **kwargs)


class LabelFeedBack(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        )

    qr_label = models.ForeignKey(
        QrLabel, 
        on_delete=models.CASCADE,
        verbose_name = "标签",
        )

    feed_back = models.TextField(
        verbose_name="反馈内容",
        default = "无",
        )

    contact = models.CharField(
        max_length=200,
        verbose_name="联系方式",
        default = "无",
        )


    user = models.CharField(
        max_length=200,
        verbose_name="人员",
        default = "",
        )


    upload_img_url = models.URLField(
        verbose_name = '图片',
        blank = True,
        )

    is_show = models.BooleanField(
        verbose_name = '是否显示',
        default = True,
        )

    date_time = models.DateTimeField(
        verbose_name = '时间',
        default=datetime.now(),
        blank=True
        )

    ip = models.GenericIPAddressField(
        verbose_name = 'IP',
        default = '0.0.0.0',
        )

    handled = models.BooleanField(
        default = False,
        verbose_name = "处理",
        )

    def __str__(self):
        return "%s %s %s" % (self.date_time, 
            self.feed_back,
            self.handled,
            )

    class Meta():
        verbose_name = "标签反馈"
        verbose_name_plural = '4.标签反馈'
        ordering = ['date_time']


class ScanRecord(models.Model):
    qr_label = models.ForeignKey(QrLabel, on_delete=models.CASCADE)

    ip = models.GenericIPAddressField(
        verbose_name="IP地址",
        )
    json = models.CharField(max_length=900,
         default="",
         )
    city = models.CharField(max_length=200,
        verbose_name="城市",
        default="",
        )
    scan_date = models.DateTimeField(auto_now_add=True,
        verbose_name="扫描时间",
        ) 

    def __str__(self):
        return "%s" % (self.scan_date, )

    class Meta():
        verbose_name = "扫码记录"
        verbose_name_plural = '5.扫码记录'

