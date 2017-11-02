#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster
from django.shortcuts import render


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request,qrcode):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(qrcode = qrcode) 
        print(qr_label.qrcode)
        qr_label.scaned(get_client_ip(request))
        print(qr_label.get_first_scan())
        data_master = qr_label.data_master
        context = {'qr_label': qr_label,'data_master':data_master}
        
        return render(request, 'v1/qrscan.html', context)
    except:
        pass

    return HttpResponse(response)

