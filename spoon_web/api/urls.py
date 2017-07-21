from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_keys$', views.get_keys),
    url(r'^fetchone_from', views.fetchone_from),
    url(r'^fetchall_from', views.fetchall_from),
]