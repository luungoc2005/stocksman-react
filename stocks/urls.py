from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # get stock
    url(r'^get_stock/(?P<stock_code>[a-zA-Z0-9]{3})/$', views.get_stock),
    # find stock
    url(r'^find_stock/(?P<code>[a-zA-Z0-9]+)/(?:(?P<limit>\d+))$', views.find_stock),
    # top stocks
    url(r'^top_stocks/(?:(?P<timestamp>\d+))/(?:(?P<limit>\d+))$', views.top_stocks),
    url(r'^top_stocks/(?:(?P<timestamp>\d+))$', views.top_stocks),
]