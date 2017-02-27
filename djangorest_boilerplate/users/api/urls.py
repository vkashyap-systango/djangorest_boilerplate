from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^users/login/$', views.IndexPageView.as_view()),
    url(r'^users/fb_login_success/$', views.SocialLoginView.as_view()),
]
