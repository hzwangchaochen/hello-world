from django.conf.urls import url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^sceneResult/(?P<tablename>\w+)/$',views.sceneResult),
    url(r'^getFileContent/$',views.getFileContent),
    url(r'^findAllSqlName/(?P<projectname>\w+)/$',views.findAllSqlName),
    url(r'^getDataFromMysql/$',views.getDataFromMysql),
    url(r'^deleteEntry/(?P<entryname>\w+)/$',views.deleteEntry),
    url(r'^drawResult/(?P<tablename>\w+)/$',views.drawResult),
    url(r'^getResultAll/$',views.getResultAll),
    url(r'^drawResultAll/$',views.drawResultAll),
    url(r'^drawMEMResult/(?P<tablename>\w+)/$',views.drawMEMResult),
    url(r'^uploadLog/$',views.uploadLog),
    url(r'^downloadFile/$',views.downloadFile),
    url(r'^exportToExcel/(?P<tablename>\w+)/$',views.exportToExcel),
    url(r'^exportLogToTxt/(?P<tablename>\w+)/$',views.exportLogToTxt),

    url(r'^uploadFile/$',views.uploadFile),
    url(r'^uploadFilePage/$',views.uploadFilePage)

]
