from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    url(r'^users/signup/$', views.SignUp.as_view()),
    url(r'^users/index/$', views.IndexPageView.as_view()),
    url(r'^users/login/$', views.LoginView.as_view()),
    url(r'^users/logout/$', views.LogoutView.as_view()),  
    url(r'^users/user_details/$', views.SocialLoginView.as_view()),
    url(r'^users/password/reset/$', views.ResetPassword.as_view()),
    url(r'^users/password/reset/confirm/(?P<password_reset_token>[A-Za-z0-9\-]+)/$', views.ConfirmPasswordReset.as_view()),

]
