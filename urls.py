from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/$', views.qrscan, name='qrscan'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/label-scan-list/$', views.label_scan_list, name='label_scan_list'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/setdm/$', views.set_data_master, name='set_data_master'),
    url(r'^get-datamaster-list/$', views.get_datamaster_list, name='get_datamaster_list'),
    url(r'^new/(?P<num>\d{1,4})/$', views.get_new_labels, name='get_new_labels'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/setdm/get-datamaster-detail/$', views.get_datamaster_detail, name='get_datamaster_detail'),
]
