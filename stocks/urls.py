from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # get stock
    url(r'^get_stock/(?P<stock_code>[a-zA-Z0-9]+)/?$', views.get_stock),
    # ref data
    url(r'^ref/get_indices/?$', views.get_indices),
    # find stock
    url(r'^find_stock/(?P<code>[a-zA-Z0-9]+)/(?:(?P<limit>\d+))/?$', views.find_stock),
    # top stocks
    url(r'^top_stocks(?:/(?P<filter>[a-zA-Z]+))?(?:/(?P<timestamp>\d+))?(?:/(?P<limit>\d+))?/$',
        views.top_stocks, {'t3': False}),
    url(r'^top_stocks_t3(?:/(?P<filter>[a-zA-Z]+))?(?:/(?P<timestamp>\d+))?(?:/(?P<limit>\d+))?/$',
        views.top_stocks, {'t3': True}),
    # events
    url(r'^events/?$', views.get_events),
    # predictions
    url(r'^project_stock/(?P<stock_code>[a-zA-Z0-9]+)/?$', views.project_stock),
    url(r'^project_all/(?:(?P<timestamp>\d+))?/?$', views.project_all),
    # status/maintenance
    url(r'^status/?$', views.get_update_status),
    url(r'^update_all/?$', views.update_data),
]
