from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # get stock
    url(r'^get_stock/(?P<stock_code>[a-zA-Z]{3})/$', views.get_stock),
    # find stock
    url(r'^find_stock/(?P<code>[a-zA-Z]+)/(?:(?P<limit>\d+))$', views.find_stock),
]