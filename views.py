#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster,ScanRecord
from django.shortcuts import render
from django.views.decorators import csrf
from django.core.files.storage import FileSystemStorage
import uuid
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.http import StreamingHttpResponse
import requests
import time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request, uuid):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        print(qr_label.qrcode)
        qr_label.scaned(get_client_ip(request))
        data_master = qr_label.data_master
        context = {'qr_label': qr_label,'data_master':data_master}
        print('ok1')        
        print(context)
        return render(request, 'v1/qrscan.html', context)
    except:
        pass

    return HttpResponse(response)

def ipdetail(request, uuid):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        qr_label.scaned(get_client_ip(request))
        data_master = qr_label.data_master
        scan_records = ScanRecord.objects.filter(qr_label = qr_label).order_by('-scan_date')
        context = {'qr_label': qr_label,'data_master':data_master,'scan_records':scan_records}
        return render(request, 'v1/ipdetail.html', context)
    except:
        pass

    return HttpResponse(response)

def setdatamaster(request,uuid):
    response = "not exist"
    try:
        data_master =  DataMaster.objects.get(master_uuid = uuid)
        if request.POST:
            data_master.title = request.POST['title']
            data_master.describe = request.POST['describe']
            data_master.tel = request.POST['tel']
            try:
                if request.FILES['img']:
                    myfile = request.FILES['img']
                    fs = FileSystemStorage()
                    filename = fs.save(myfile.name, myfile)
                    data_master.img_url = fs.url(filename)
            except:
                pass
            data_master.save()
        else:
            pass
        ctx = {'data_master':data_master,}
        print("ok63")
        return render(request, "v1/setdatamaster.html", ctx)
    except:
        pass
    return HttpResponse(response)

@staff_member_required
def getlabel(request, m_code, num):
    try:
        name_space = uuid.NAMESPACE_DNS
        master_code = m_code
        master_uuid = str(uuid.uuid5(name_space,str(master_code)))
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
        print(len(num))
        print(10**len(num))
        print("----------")
        qrcode_base = int(master_code)* (10**len(num))
        print(qrcode_base)
        for x in range(0, int(num)):
            qrcode = qrcode_base + x
            label_uuid = str(uuid.uuid5(name_space,str(qrcode)))
            qrlabel = QrLabel(data_master = md,
                qrcode = str(qrcode),
                label_uuid = label_uuid,
                )
            qrlabel.save()
        print("ok105")
        context = {'qr_labels': QrLabel.objects.filter(data_master = md).order_by("qrcode"),
            'data_master':md,}
        return render(request, 'v1/label_list.html', context)
    except:
        return HttpResponse("404")

class JSONObject:
    def __init__(self, d):
        self.__dict__ = d

@staff_member_required
def getip(request):
    scan_records = ScanRecord.objects.all() 
    for sr in scan_records:
        sr.json = requests.get("http://ip.taobao.com/service/getIpInfo.php?ip="+str(sr.ip)).text
        sr.city = json.loads(sr.json, object_hook=JSONObject).data.city
        sr.save()
    return HttpResponse("ok")

