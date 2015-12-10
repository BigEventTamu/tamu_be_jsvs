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
from django.contrib.auth import views as auth_views

from job_site_verification import views


urlpatterns = [
    url(r'^$', views.Index.as_view(), name="index"),
    url(r'^forms/$', views.FormList.as_view(), name="list-forms"),

    url(r'^forms/([0-9]+)/$', views.JobRequestFormList.as_view(), name="select-job-request-form"),
    url(r'^forms/([0-9]+)/([0-9]+)/$', views.JobRequestForm.as_view(), name="job-request-form"),

    url(r'^forms/edit-service-forms/$', views.EditServiceFormList.as_view(), name="edit-service-form-list",),
    url(r'^forms/edit-service-forms/([0-9]+)/$', views.EditServiceForm.as_view(), name="edit-service-form"),

    url(r'^forms/edit-service-forms/([0-9]+)/choices/$', views.EditServiceFormChoices.as_view(),
        name="edit-service-form-choices"),

    url(r'^accounts/login/$', auth_views.login, name="login"),
    url(r'^accounts/logout/$', auth_views.logout, name="logout"),

    url(r'^json/get-token/$', views.AuthJSON.as_view(), name="auth-json"),
    url(r'^json/jobstubs/$', views.JobStubListJSON.as_view(), name="jobstubs-json"),
    url(r'^json/services/$', views.ServiceListJSON.as_view(), name="service-list-json"),
    url(r'^json/formtypes/$', views.FormTypeListJSON.as_view(), name="formtype-list-json"),
    url(r'^json/form/([0-9]+)/$', views.FormListJSON.as_view(), name="form-list-json"),
    url(r'^json/form/([0-9]+)/([0-9]+)/$', views.FormDetailJSON.as_view(), name="form-detail-json"),
]
