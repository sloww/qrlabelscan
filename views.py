#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster,ScanRecord,LabelRecord,LabelFeedBack
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from django.core.files.storage import FileSystemStorage
import uuid
from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse
from qqwry import QQwry
import time
import os
import shutil
import oss2
from django.conf import settings                    
from django.utils.timezone import utc
from datetime import datetime
import qrcode


def name():
    t = datetime.now()
    return '{}{}{}{}{}{}{}'.format(
        t.year,
        t.month,
        t.day,
        t.hour,
        t.minute,
        t.second,
        t.microsecond,
        )

def get_qr_img_url(qrstr,box_size):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
        )
    qr.add_data(qrstr)
    qr.make(fit=True)

    img = qr.make_image()
    img_name ='{}.{}'.format(name(),'png')
    img_fullname = '{}/{}'.format(settings.MEDIA_ROOT,img_name)
    print(img_fullname)
    img.save(img_fullname)
    return img_name


def get_qr(request,box_size,qrstr):
    qrstr = qrstr.replace(':/','://') 
    c = "<img src ='/media/{}'/>".format(get_qr_img_url(qrstr,box_size),)
    return HttpResponse(c)

 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def add_scan_record(qr_label,ip):
    q = QQwry()
    sr = ScanRecord()
    sr.ip = ip
    sr.scan_date = datetime.now()
    sr.qr_label = qr_label
    if q.load_file(settings.QQPATH):
        sr.json = q.lookup(str(ip))
        sr.city = sr.json[0]
    sr.save()



def index(request):
    return HttpResponse("欢迎使用手机扫码平台")

def get_img_url(request):
    new_name = ''
    if request.FILES['img']:
        try:
            bucket = oss2.Bucket(oss2.Auth(settings.ACCESS_KEY_ID,
                settings.ACCESS_KEY_SECRET), settings.ENDPOINT, settings.BUCKET_NAME)
            myfile = request.FILES['img']
            t0 = datetime(1, 1, 1)
            now = datetime.utcnow()
            seconds = (now - t0).total_seconds()* 100000
            new_name = qr_label.qrcode + str(seconds) + os.path.splitext(myfile.name)[1]
            bucket.put_object(new_name, myfile)
        except:
            pass
    return settings.IMGPREURL + new_name


## 二维码扫描处理
def qrscan_template(request, uuid, template):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        add_scan_record(qr_label, get_client_ip(request))
        data_master = qr_label.data_master
        lfb = LabelFeedBack()
        if data_master.redirect_on:
            agent =request.META['HTTP_USER_AGENT'].lower()
            if 'micromessenger' in agent:
                return redirect(data_master.redirect_url_wx)
            if 'alipayclient' in agent:
                return redirect(data_master.redirect_url_tb)
            if 'aliapp' in agent:
                return redirect(data_master.redirect_url_tb)
            #临时占位符，非有效
            if 'jd' in agent:
                return redirect(data_master.redirect_url_jb)
            return redirect(data_master.redirect_url)
        else:
            if request.POST:
                if data_master.sales_on and 'sale' in request.POST.keys():
                    qr_label.mark_date=datetime.now()
                    qr_label.equip_no = request.POST['equip_no']
                    lfb.equip_img_url = get_img_url(request) 
                    qr_label.has_sale = True
                    qr_label.save()
                if data_master.feedback_show and 'feedback' in request.POST.keys():
                    lfb.qr_label = qr_label
                    lfb.feed_back = request.POST['feed_back']
                    lfb.contact = request.POST['contact']
                    try:
                        if request.FILES['img']:
                            bucket = oss2.Bucket(oss2.Auth(settings.ACCESS_KEY_ID, 
                                settings.ACCESS_KEY_SECRET), settings.ENDPOINT, settings.BUCKET_NAME)
                            myfile = request.FILES['img']
                            new_name = qr_label.qrcode + name() + os.path.splitext(myfile.name)[1]
                            bucket.put_object(new_name, myfile)
                            lfb.upload_img_url = settings.IMGPREURL + new_name
                    except:
                        pass
                    lfb.save()
            lfbs = LabelFeedBack.objects.filter(qr_label = qr_label).filter(is_show = True).order_by('date_time')
            context = {'qr_label': qr_label,'data_master':data_master,'lfbs':lfbs}  
            if template:
                return render(request, template, context)
            else:
                return render(request, data_master.template, context)
    except:
        pass

    return HttpResponse(response)

def qrscan(request, uuid):
    return qrscan_template(request, uuid, '')


def qrscan_edit(request, uuid):
    return qrscan_template(request, uuid, 'v1/qrscan.html')

def post(request, id):
    try:
        lfb = LabelFeedBack.objects.get(id=id)
        print(id)
        context = {'lfb':lfb,}
        return render(request, 'v1/post.html', context)
        
    except:
        return HttpResponse("not exist")

@staff_member_required
def get_lfbs(request, master_uuid):
    try:
        lfbs = LabelFeedBack.objects.filter(qr_label__data_master__master_uuid = master_uuid)
        dm = DataMaster.objects.get(master_uuid = master_uuid)
        context = {'lfbs':lfbs,'dm':dm,'admin_url':'myadmin'}
        return render(request, 'p/fb.html', context)
    except:
        return HttpResponse("not exist")


def delete_post(request, no, id):
    print('删除评论-开始')
    if LabelFeedBack.objects.filter(id = id):
        p = LabelFeedBack.objects.filter(id = id)[0]
        p.is_show = False
        p.save()
        print('ok')
    url = "/a/{}/edit/".format(no)
    print('删除评论')
    return redirect(url)
    

def label_scan_list(request, uuid):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        data_master = qr_label.data_master
        scan_records = ScanRecord.objects.filter(qr_label = qr_label).order_by('-scan_date')
        context = {'qr_label': qr_label,'data_master':data_master,'scan_records':scan_records}
        return render(request, 'v1/label-scan-list.html', context)
    except:
        pass

    return HttpResponse(response)

def set_data_master(request,uuid):
    response = "not exist"
    try:
        data_master =  DataMaster.objects.get(master_uuid = uuid)
        if request.POST:
            data_master.title = request.POST['title']
            data_master.describe = request.POST['describe']
            data_master.tel = request.POST['tel']
            data_master.company = request.POST['company']
            data_master.redirect_url = request.POST['redirect_url']
            if 'title_show' in request.POST.keys():
                data_master.title_show  = True
            else:
                data_master.title_show  = False 
            if 'img_show' in request.POST.keys():
                data_master.img_show  = True
            else:
                data_master.img_show  = False 
            if 'scan_show' in request.POST.keys():
                data_master.scan_show  = True
            else:
                data_master.scan_show  = False 
            if 'redirect_on' in request.POST.keys():
                data_master.redirect_on  = True
            else:
                data_master.redirect_on  = False 
            if 'describe_show' in request.POST.keys():
                data_master.describe_show  = True
            else:
                data_master.describe_show  = False 

            try:
                if request.FILES['img']:
                    bucket = oss2.Bucket(oss2.Auth(settings.ACCESS_KEY_ID, 
                        settings.ACCESS_KEY_SECRET), settings.ENDPOINT, settings.BUCKET_NAME)
                    myfile = request.FILES['img']
                    new_name = data_master.master_code+ os.path.splitext(myfile.name)[1]
                    bucket.put_object(new_name, myfile)
                    #fs = FileSystemStorage()
                    #filename = fs.save(myfile.name, myfile)
                    #data_master.img_url = fs.url(filename)
                    data_master.img_url = settings.IMGPREURL + new_name
            except:
                pass
            data_master.save()
        else:
            pass
        ctx = {'data_master':data_master,}
        return render(request, "v1/set-data-master.html", ctx)
    except:
        pass
    return HttpResponse(response)


@staff_member_required

def get_label_list(request, master_code):
    dm = DataMaster.objects.get(master_code = master_code)
    con=""
    if dm:
        labels = QrLabel.objects.filter(data_master = dm).order_by('-label_code')
        for label in labels:
            con = con + settings.URLPRE + '%s/,%s,%s<br>' % (label.label_uuid,dm.master_code,label.label_code)
    return HttpResponse(con) 

@staff_member_required

def qrlabel_reset_url(request):
    labels = QrLabel.objects.filter(url__isnull = True)[0:1000]
    for l in labels:
        l.save()
    con="ok"
    return HttpResponse(con) 


@staff_member_required

def get_datamaster_list(request):
    dms = DataMaster.objects.order_by('master_code')
    con=""
    for dm in dms:
        con = con + settings.URLPRE + '%s/setdm/,%s <br>' % (dm.master_uuid, dm.master_code,)  
    return HttpResponse(con) 

@staff_member_required
def get_scanrecord_list(request, num):
    context = {'srs':ScanRecord.objects.order_by('-scan_date')[:int(num)] ,}
    return render(request, 'v1/get-scanrecord-list.html', context)


@staff_member_required
def get_scanrecord_list_by_mastercode(request,master_code,num,):
    dm = DataMaster.objects.get(master_code = master_code)
    srs=ScanRecord.objects.filter(qr_label__data_master__master_code = master_code).order_by('-scan_date')[:int(num)]

    context = {'srs':srs,'dm':dm,'admin_url':'myadmin'}
    return render(request, 'p/scanlist.html', context)



def get_datamaster_detail(request, uuid):
    dm = DataMaster.objects.get(master_uuid=uuid)
    labels = QrLabel.objects.filter(data_master = dm).order_by('label_code')
    context = {'qrlabels':labels,
        'data_master':dm,}
    return render(request, 'v1/get-datamaster-detail.html', context)



@staff_member_required
def get_new_labels_g(request,num,is_short):
    try:
        label_record = LabelRecord.objects.order_by('master_code').last()
        name_space = uuid.NAMESPACE_DNS
        master_code = '10000001' 
        lr = LabelRecord()
        if LabelRecord.objects.order_by('master_code').count()>0:
            master_code = str(label_record.master_code+1).rjust(8,'0')
            lr.master_code = label_record.master_code +1
        else:
            lr.master_code=10000001
        lr.label_code = int(num)
        lr.save()
        master_uuid = str(uuid.uuid5(name_space,master_code))
        title = "公司名称"
        describe = "您查询的是正品，请放心使用。有任何技术问题，可拨打 021-50687572 或加 QQ群 590646661 进行咨询！"
        tel = "021-50687572"
        img_url = "http://tslink-cc.oss-cn-hangzhou.aliyuncs.com/pub/noimage.png"
        md = DataMaster(master_uuid = master_uuid,
            master_code = master_code,
            title = title,
            describe = describe,
            tel = tel,
            img_url = img_url,
            ) 
        md.save() 
        t = int(num)+1
        for x in range(1, t):
            label_code =  str(x).rjust(8,'0')
            qrcode = master_code + label_code
            if is_short:
                label_uuid = qrcode
            else:
                label_uuid = str(uuid.uuid5(name_space, qrcode))
            qrlabel = QrLabel(data_master = md,
                qrcode = qrcode,
                label_code = label_code,
                label_uuid = label_uuid,
                )
            qrlabel.save()
        context = {'qr_labels': QrLabel.objects.filter(data_master = md).order_by("qrcode"),
            'data_master':md,}
        return render(request, 'v1/get-new-labels.html', context)
    except:
        return HttpResponse("404")


@staff_member_required
def get_new_labels(request,num):
    return get_new_labels_g(request,num,False)

@staff_member_required
def get_new_labels_s(request,num):
    return get_new_labels_g(request,num,True)

#暂时没有使用
@staff_member_required
def copy_dm(request,master_uuid):
    try:
        label_record = LabelRecord.objects.order_by('master_code').last()
        name_space = uuid.NAMESPACE_DNS
        master_code = '10000001' 
        lr = LabelRecord()
        if LabelRecord.objects.order_by('master_code').count()>0:
            master_code = str(label_record.master_code+1).rjust(8,'0')
            lr.master_code = label_record.master_code +1
        else:
            lr.master_code=10000001
        lr.label_code = int(num)
        lr.save()
        master_uuid = str(uuid.uuid5(name_space,master_code))
        title = "公司名称"
        describe = "您查询的是正品，请放心使用。有任何技术问题，可拨打 021-50687572 或加 QQ群 590646661 进行咨询！"
        tel = "021-50687572"
        img_url = "http://tslink-cc.oss-cn-hangzhou.aliyuncs.com/pub/noimage.png"
        md = DataMaster(master_uuid = master_uuid,
            master_code = master_code,
            title = title,
            describe = describe,
            tel = tel,
            img_url = img_url,
            ) 
        md.save() 
        t = int(num)+1
        for x in range(1, t):
            label_code =  str(x).rjust(8,'0')
            qrcode = master_code + label_code
            label_uuid = str(uuid.uuid5(name_space, qrcode))
            qrlabel = QrLabel(data_master = md,
                qrcode = qrcode,
                label_code = label_code,
                label_uuid = label_uuid,
                )
            qrlabel.save()
        context = {'qr_labels': QrLabel.objects.filter(data_master = md).order_by("qrcode"),
            'data_master':md,}
        return render(request, 'v1/get-new-labels.html', context)
    except:
        return HttpResponse("404")
