from django.conf.urls import url
from django.urls import path, re_path


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<uuid>/', views.qrscan, name='qrscan'),
    path('<uuid>/edit/', views.qrscan_edit, name='qrscan_edit'),
    path('<uuid>/label-scan-list/', views.label_scan_list, name='label_scan_list'),
    path('<uuid>/setdm/', views.set_data_master, name='set_data_master'),
    path('get-datamaster-list/', views.get_datamaster_list, name='get_datamaster_list'),
    path('qrlabel-reset-url/', views.qrlabel_reset_url, name='qrlabel_reset_url'),
    path('scanlist/<int:num>/', views.get_scanrecord_list, name='get_scanrecord_list'),
    re_path(r'^qr/(?P<box_size>\d{1,2})/(?P<qrstr>\S+)$', views.get_qr, name='get_qr'),
    path('scanlist/<int:master_code>/<int:num>/', views.get_scanrecord_list_by_mastercode, name='get_scanrecord_list_by_mastercode'),
    url(r'^new/(?P<num>\d{1,4})/$', views.get_new_labels, name='get_new_labels'),
    url(r'^new/s/(?P<num>\d{1,4})/$', views.get_new_labels_s, name='get_new_labels_s'),
    url(r'^get-label-list/(?P<master_code>\d{8})/$', views.get_label_list, name='get_label_list'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/setdm/get-datamaster-detail/$', views.get_datamaster_detail, name='get_datamaster_detail'),
    url(r'^(?P<master_uuid>[0-9A-Fa-f-]+)/feedback/$', views.get_lfbs, name='get_lfbs'),
    url(r'^post/(?P<id>[0-9A-Fa-f-]+)/$', views.post, name='post'),
    url(r'^d/(?P<no>[0-9A-Fa-f-]+)/(?P<id>[0-9A-Fa-f-]+)/$', views.delete_post, name='delete_post'), 
]

