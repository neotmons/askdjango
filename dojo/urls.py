# blog/urls.py

from django.conf.urls import url
from dojo import views

urlpatterns = [
    url(r'^sum/(?P<numbers>[\d/]+)/$', views.mysum),
]