from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from .views import RegistrationAPIView, LoginAPIView, UserRetrieveUpdateAPIView

from django.contrib.auth import views as auth_views
urlpatterns = [

    url('users/login/', LoginAPIView.as_view()),
    url('users/register/', RegistrationAPIView.as_view()),
    url('user/', UserRetrieveUpdateAPIView.as_view()),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),

    # url('user/change_password/', Change_Password.as_view()),
    # url('user/reset_password/',  Email.as_view())

]
