from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^getDataFromMysql/$',views.getDataFromMysql),
    url(r'^updateDataToMysql/$',views.updateDataToMysql),
    url(r'^searchDataFromMysql/$',views.searchDataFromMysql),
    url(r'^addTestCase/$',views.addTestCase),
    url(r'^deleteTestCase/$',views.deleteTestCase),
    url(r'^exportToExcel/(?P<tablename>\w+)/$',views.exportToExcel),

    url(r'^getResult/(?P<tablename>\w+)/$',views.getResult),
    url(r'^getSubResult/(?P<tablename>\w+)/$',views.getSubResult),
    url(r'^getResultIndex/(?P<tablename>\w+)/$',views.getResultIndex),
    url(r'^findAllSqlName/(?P<projectname>\w+)/$',views.findAllSqlName),

    url(r'^getTrend/(?P<projectname>\w+)/$',views.getTrend),
    url(r'^getTrendSub/$',views.getTrendSub),
    url(r'^getTrendAll/$',views.getTrendAll),
    url(r'^getTrendAllIndex/$',views.getTrendAllIndex),

    url(r'^scenePC/$',views.scenePC),
    url(r'^sceneIndex/$',views.sceneIndex),

]
