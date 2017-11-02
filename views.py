#coding:utf-8

from django.http import HttpResponse
from .models import QrLabel, DataMaster
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request,qrcode):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(qrcode = qrcode) 
        qr_label.scaned()
        qr_label.scaned_time()
        data_master = qr_label.data_master
        context = {'qr_label': qr_label,'data_master':data_master}
        
        return render(request, 'v1/qrscan.html', context)
    except:
        pass

    return HttpResponse(response)

