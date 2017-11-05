#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster,ScanRecord
from django.shortcuts import render
from django.views.decorators import csrf


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request, qrcode):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(qrcode = qrcode) 
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

def ipdetail(request, qrcode):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(qrcode = qrcode) 
        qr_label.scaned(get_client_ip(request))
        data_master = qr_label.data_master
        scan_records = ScanRecord.objects.filter(qr_label = qr_label).order_by('-scan_date')
        context = {'qr_label': qr_label,'data_master':data_master,'scan_records':scan_records}
        return render(request, 'v1/ipdetail.html', context)
    except:
        pass

    return HttpResponse(response)

def setdatamaster(request,master_code):
    response = "not exist"
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['title']
    else:
        pass
    print('num 57')
    print(ctx)
    return render(request, "v1/setdatamaster.html", ctx)

