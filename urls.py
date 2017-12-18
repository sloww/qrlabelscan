from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/$', views.qrscan, name='qrscan'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/edit/$', views.qrscan_edit, name='qrscan_edit'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/label-scan-list/$', views.label_scan_list, name='label_scan_list'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/setdm/$', views.set_data_master, name='set_data_master'),
    url(r'^get-datamaster-list/$', views.get_datamaster_list, name='get_datamaster_list'),
    url(r'^qrlabel-reset-url/$', views.qrlabel_reset_url, name='qrlabel_reset_url'),
    url(r'^get-scanrecord-list/(?P<num>\d{1,4})/$', views.get_scanrecord_list, name='get_scanrecord_list'),
    url(r'^new/(?P<num>\d{1,4})/$', views.get_new_labels, name='get_new_labels'),
    url(r'^get-label-list/(?P<master_code>\d{8})/$', views.get_label_list, name='get_label_list'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/setdm/get-datamaster-detail/$', views.get_datamaster_detail, name='get_datamaster_detail'),
    url(r'^(?P<master_uuid>[0-9A-Fa-f-]+)/feedback/$', views.get_lfbs, name='get_lfbs'),
    url(r'^post/(?P<id>[0-9A-Fa-f-]+)/$', views.post, name='post'),
    url(r'^d/(?P<no>[0-9A-Fa-f-]+)/(?P<id>[0-9A-Fa-f-]+)/$', views.delete_post, name='delete_post'), 
]

