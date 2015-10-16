"""tamu_be_jsvs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url

from job_site_verification import views


urlpatterns = [
    url(r'^json/get-token/$', views.AuthJSON.as_view(), name="auth-json"),
    url(r'^json/services/$', views.ServiceListJSON.as_view(), name="service-list"),
    url(r'^json/formtypes/$', views.FormTypeListJSON.as_view(), name="formtype-list"),
    url(r'^json/form/([0-9]+)/$', views.FormListJSON.as_view(), name="form-list"),
    url(r'^json/form/([0-9]+)/([0-9]+)/$', views.FormDetailJSON.as_view(), name="form-detail"),
]
