from django.http import HttpResponse

from .models import QrLabel, DataMaster

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request,qrcode):
    response = "not exist"
    try:
        qr_label = QrLabel.objects.get(qrcode = qrcode) 
        data_master = qr_label.data_master
        response = "<p>%s</p><p> 题目： %s</p><p> 描述：%s</p> <p>电话：%s</p> " % (qr_label.qrcode,data_master.title, data_master.describe,data_master.tel)
    except OSError:
        pass

    return HttpResponse(response)

