from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', admin.site.admin_view(views.UwsgiStatus.as_view()),
        name='uwsgi_index'),
    re_path(r'^reload/$', admin.site.admin_view(views.UwsgiReload.as_view()),
        name='uwsgi_reload'),
    re_path(r'^cache_clear/$', admin.site.admin_view(
        views.UwsgiCacheClear.as_view()), name='uwsgi_cache_clear'),
    re_path(r'^log/$', admin.site.admin_view(views.UwsgiLog.as_view()),
        name='uwsgi_log'),
    re_path(r'^signal/$', admin.site.admin_view(views.UwsgiSignal.as_view()),
        name='uwsgi_signal'),
]
