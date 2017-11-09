from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/$', views.qrscan, name='qrscan'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/ipdetail/$', views.ipdetail, name='ipdetal'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/sdm/$', views.setdatamaster, name='setdatamaster'),
    url(r'^(?P<m_code>\d{12})/(?P<num>\d{1,4})/$', views.getlabel, name='getlabel'),
    url(r'^getip/$', views.getip, name='getip'),
    url(r'^getdm/$', views.getdm, name='getdm'),
    url(r'^new/(?P<num>\d{1,4})/$', views.getnewlabels, name='getnewlabels'),
]
