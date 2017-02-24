from django.conf.urls import include, url
from . import api
urlpatterns = [
    url(r'^api/', include('users.api.urls')),
]
