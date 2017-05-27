from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^getDataFromMysql/$', views.getDataFromMysql),
    url(r'^searchDataFromMysql/$', views.searchDataFromMysql),
    url(r'^updateDataToMysql/$', views.updateDataToMysql),
    url(r'^findAllSqlName/$', views.findAllSqlName),
    url(r'^deleteTable/(?P<tablename>\w+)/$', views.deleteTable),
    url(r'^exportToExcel/(?P<tablename>\w+)/$', views.exportToExcel),
    url(r'^getTotalResult/(?P<tablename>\w+)/$', views.getTotalResult),
    url(r'^getResultIndex/(?P<tablename>\w+)/$', views.getResultIndex),
    url(r'^getSubResult/(?P<tablename>\w+)/$', views.getSubResult)
]
