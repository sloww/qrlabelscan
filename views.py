from django.http import HttpResponse

from .models import Qr

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def qrscan(request,qrcode):
    response = "not exist"
    if Qr.objects.filter(qrcode = qrcode).exists():
        qr = Qr.objects.get(qrcode = qrcode) 
        response = "qr: %s." % qr.company_name
    return HttpResponse(response)

