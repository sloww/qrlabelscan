#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster,ScanRecord,LabelRecord
from django.shortcuts import render
from django.views.decorators import csrf
from django.core.files.storage import FileSystemStorage
import uuid
from django.contrib.admin.views.decorators import staff_member_required
from django.http import StreamingHttpResponse
from qqwry import QQwry
import time

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return HttpResponse("欢迎使用手机扫码平台")

def qrscan(request, uuid):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(label_uuid = uuid) 
        qr_label.scaned(get_client_ip(request))
        data_master = qr_label.data_master
        context = {'qr_label': qr_label,'data_master':data_master}

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
    q = QQwry()
    if q.load_file('qqwry.dat'):
        scan_records = ScanRecord.objects.all() 
        for sr in scan_records:
            sr.json = q.lookup(str(sr.ip)) 
            sr.city = sr.json[0]
            sr.save()
    return HttpResponse("finish")


@staff_member_required
def getdm(request):
    dms = DataMaster.objects.order_by('master_code')
    con=""
    for dm in dms:
        con = con + 'http://tslink.cn/v1/%s/,%s <br>' % (dm.master_uuid, dm.master_code,)  
    return HttpResponse(con) 


@staff_member_required
def getnewlabels(request,num):
    try:
        label_record = LabelRecord.objects.order_by('master_code').last()
        name_space = uuid.NAMESPACE_DNS
        master_code = '10000001' 
        lr = LabelRecord()
        if LabelRecord.objects.order_by('master_code').count()>0:
            print(master_code)
            print(str(label_record.master_code+1))
            master_code = str(label_record.master_code+1).rjust(8,'0')
            print(master_code)
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
        print(154)
        print(master_code)
        md = DataMaster(master_uuid = master_uuid,
            master_code = master_code,
            title = title,
            describe = describe,
            tel = tel,
            img_url = img_url,
            ) 
        md.save() 
        print(165)
        t = int(num)+1
        print(167)
        print(t)
        for x in range(1, t):
            print('ok'+str(x))
            label_code =  str(x).rjust(8,'0')
            qrcode = master_code + label_code
            label_uuid = str(uuid.uuid5(name_space, qrcode))
            qrlabel = QrLabel(data_master = md,
                qrcode = qrcode,
                label_code = label_code,
                label_uuid = label_uuid,
                )
            qrlabel.save()
            print(x)
            print(qrlabel)
        context = {'qr_labels': QrLabel.objects.filter(data_master = md).order_by("qrcode"),
            'data_master':md,}
        return render(request, 'v1/label_list.html', context)
    except:
        return HttpResponse("404")


