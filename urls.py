from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/$', views.qrscan, name='qrscan'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/ipdetail$', views.ipdetail, name='ipdetal'),
    url(r'^(?P<uuid>[0-9A-Fa-f-]+)/sdm$', views.setdatamaster, name='setdatamaster'),
]
