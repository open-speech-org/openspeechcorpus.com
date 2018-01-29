# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Log in
    url(
        r'log-in/$',
        auth_views.login,
        {
            'template_name': 'authentication/log-in.html',
        },
        name='log-in'
    ),

    url(
        r'log-out/$',
        auth_views.logout,
        {
            'next_page': '/'
        },
        name='log-out'
    ),

    # Sign Up
    url(
        r'sign-up/$',
        views.SignUp.as_view(),
        name='sign-up'
    ),
    url(
        r'sign-up-confirm/(?P<token>\w+)/$',
        views.SignUpConfirm.as_view(),
        name='sign-up-confirm'
    ),

    # Change Password
    url(
        r'change-password/$',
        auth_views.password_change,
        {
            'template_name': 'authentication/change-password.html',
        },
        name='change-password'
    ),
    url(
        r'change-password-done/$',
        auth_views.password_change_done,
        {
            'template_name': 'authentication/change-password-success.html',
            },
        name='password_change_done'
    ),

    # Password Recovery
    url(
        r'recover-password/$',
        auth_views.password_reset,
        {
            'template_name': 'autenticacion/recover-password.html',
            'email_template_name': 'authentication/email-restore-password.html',
            'post_reset_redirect': reverse_lazy('password_reset_done')
        },
        name='password_reset'
    ),
    url(
        r'recover-password-done/$',
        auth_views.password_reset_done,
        {
            'template_name': 'authentication/recover-password-success.html',
            },
        name='password_reset_done'
    ),


    url(
        r'reset-password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'authentication/reset-password.html',
        },
        name='password_reset_confirm'),
    url(
        r'reset-password-done/$',
        auth_views.password_reset_complete,
        {
            'template_name': 'authentication/change-password-success.html',
        },
        name='password_reset_complete'),


]
