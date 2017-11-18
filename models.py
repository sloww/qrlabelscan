#coding:utf-8   

from django.db import models
import uuid

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
        verbose_name_plural = '申请记录'

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
        verbose_name="备注",
        )
    distributor = models.CharField(max_length=200,
        default="",
        verbose_name="经销商",
        )

    img_url = models.URLField(max_length=200,
        verbose_name="主图地址",
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
        verbose_name="文字描述",
        )

    scan_show = models.BooleanField(default = True,
        verbose_name = '是否显示扫描结果',
        )

    describe_show = models.BooleanField(default = True,
        verbose_name = '是否显示描述信息',
        )
    feedback_show = models.BooleanField(default = False,
        verbose_name = '是否开启标签反馈模块',
        )

    tel = models.CharField(max_length=200,
        verbose_name="电话",
        )

    def __str__(self):
        return "%s ( %s )" % (self.master_code,self.title)

    class Meta():
        verbose_name = "模版"
        verbose_name_plural = '模版'

    def label_count(self):
        return  QrLabel.objects.filter(data_master=self).count()

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

    def __str__(self):
        return "%s ( %s )" % (self.qrcode, self.data_master.master_code)

    class Meta():
        verbose_name = "标签"
        verbose_name_plural = '标签'

    def scaned_times(self):
        return  ScanRecord.objects.filter(qr_label=self).count()

    def get_first_scan(self):
        return ScanRecord.objects.filter(qr_label=self).order_by('scan_date').first()


class LabelFeedBack(models.Model):

    qr_label = models.ForeignKey(
        QrLabel, 
        on_delete=models.CASCADE,
        verbose_name = "标签",
        )

    feed_back_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="反馈时间",
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

    uploud_img_url = models.URLField(
        max_length=200,
        verbose_name="反馈照片",
        )

    handled = models.BooleanField(
        default = False,
        verbose_name = "处理",
        )

    def __str__(self):
        return "%s %s %s" % (self.feed_back_date, 
            self.feed_back,
            self.handled,
            )

    class Meta():
        verbose_name = "标签反馈"
        verbose_name_plural = '标签反馈'


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
        verbose_name_plural = '扫码记录'

