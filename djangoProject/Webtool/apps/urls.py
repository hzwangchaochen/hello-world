"""Webtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from apps import views
from apps.moc import urls as moc_urls
from apps.diff import urls as diff_urls
from apps.build import urls as build_urls
from apps.regression import urls as regression_urls
from apps.server_log import urls as server_log_urls
from apps.svn_cmt_assign import urls as svn_cmt_assign_urls
from apps.conf_query import urls as conf_query_urls
from apps.info_set import urls as info_set_urls
from apps.assign_zqjt import urls as assign_zqjt_urls
from apps.assign_test_case import urls as assign_test_case_urls
from apps.unity_profiling import urls as unity_profiling_urls
from apps.analysis_performance import urls as analysis_performance_urls
from Webtool import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^openid/',include('apps.django_openid_auth.urls')),
    url(r'^$',views.index),
    url(r'^index/$',views.index),
    url(r'^moc/',include(moc_urls)),
    url(r'^diff/',include(diff_urls)),
    url(r'^build/',include(build_urls)),
    url(r'^regression/',include(regression_urls)),
    url(r'^server_log/',include(server_log_urls)),
    url(r'^svn_cmt_assign/',include(svn_cmt_assign_urls)),
    url(r'^conf_query/',include(conf_query_urls)),
    url(r'^info_set/',include(info_set_urls)),
    url(r'^assign_zqjt/',include(assign_zqjt_urls)),
    url(r'^assign_test_case/',include(assign_test_case_urls)), 
    url(r'^unity_profiling/',include(unity_profiling_urls)),
    url(r'^analysis_performance/',include(analysis_performance_urls))
]
