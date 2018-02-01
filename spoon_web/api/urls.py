from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_keys$', views.get_keys),
    url(r'^fetchone_from', views.fetchone_from),
    url(r'^fetchall_from', views.fetchall_from),
    url(r'^fetch_hundred_recent', views.fetch_hundred_recent),
    url(r'^fetch_stale', views.fetch_stale),
    url(r'^fetch_recent', views.fetch_recent),
]
