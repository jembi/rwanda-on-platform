"""openhimAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Authentication with JWT:

    # provide the most basic login/logout functionality
    url(r'^login/$', auth_views.LoginView.as_view(template_name='core/login.html'),
        name='core_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='core_logout'),

    #Custom App API's
    url(r'', include('rwandaApp.urls')),

    # enable the admin interface
    url(r'^admin/', admin.site.urls),
    url(r'^', admin.site.urls),

]
