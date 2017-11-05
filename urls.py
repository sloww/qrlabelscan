from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<qrcode>\d{16})/$', views.qrscan, name='qrscan'),
    url(r'^(?P<qrcode>\d{16})/ipdetail$', views.ipdetail, name='ipdetal'),
    url(r'^(?P<master_code>\d{12})/sdm$', views.setdatamaster, name='setdatamaster'),
]
