from django.conf.urls import include, url
from spoon_web.api.views import get_keys

urlpatterns = [
    url(r'^api/v1/', include('spoon_web.api.urls')),
]
