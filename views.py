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
    sr.qr_label = qr_label
    if q.load_file(settings.QQPATH):
        sr.json = q.lookup(str(ip))
        sr.city = sr.json[0]
    sr.save()



def index(request):
    return HttpResponse("欢迎使用手机扫码平台")

def qrscan(request, uuid):
    response = "not exist"
    try:
        print(1)
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        add_scan_record(qr_label, get_client_ip(request))
        data_master = qr_label.data_master
        lfb = LabelFeedBack()
        if data_master.redirect_on:
            return redirect(data_master.redirect_url)
        else:
            if request.POST:
                if data_master.sales_on and 'sale' in request.POST.keys():
                    qr_label.mark_date=datetime.now()
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
                            t0 = datetime(1, 1, 1)
                            now = datetime.utcnow()
                            seconds = (now - t0).total_seconds()* 100000
                            new_name = qr_label.qrcode + str(seconds) + os.path.splitext(myfile.name)[1]
                            bucket.put_object(new_name, myfile)
                            lfb.upload_img_url = settings.IMGPREURL + new_name
                    except:
                        pass
                    lfb.save()
            lfbs = LabelFeedBack.objects.filter(qr_label = qr_label).filter(is_show = True)
            context = {'qr_label': qr_label,'data_master':data_master,'lfbs':lfbs}
            return render(request, 'v1/qrscan.html', context)
    except:
        pass

    return HttpResponse(response)


def post(request, id):
    try:
        print(id)
        lfb = LabelFeedBack.objects.get(id=id)
        print(id)
        context = {'lfb':lfb,}
        return render(request, 'v1/post.html', context)
    except:
        return HttpResponse("not exist")

def delete_post(request, no, id):
    print(no)
    print(id)
    if LabelFeedBack.objects.filter(id = id):
        p = LabelFeedBack.objects.filter(id = id)[0]
        p.is_show = False
        p.save()
        print('ok')
    url = "/a/{}/".format(no)
    print(url)
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
    labels = QrLabel.objects.all()
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

def get_datamaster_detail(request, uuid):
    dm = DataMaster.objects.get(master_uuid=uuid)
    labels = QrLabel.objects.filter(data_master = dm).order_by('label_code')
    context = {'qrlabels':labels,
        'data_master':dm,}
    return render(request, 'v1/get-datamaster-detail.html', context)



@staff_member_required
def get_new_labels(request,num):
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
