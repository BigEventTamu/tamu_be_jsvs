from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.middleware import csrf
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from job_site_verification import models
from job_site_verification import forms

class AuthJSON(APIView):
    def get(self, request):
        return Response(csrf.get_token(request))

    def post(self, request):
        user = request.POST.get("username", '')
        password = request.POST.get("password", '')
        if not user or not password:
            return Response("Username or Password missing", status=status.HTTP_400_BAD_REQUEST)
        u = get_object_or_404(User, username=user)
        if not u.check_password(password):
            return Response("Username or Password incorrect.", status=status.HTTP_403_FORBIDDEN)
        if not u.is_active:
            return Response("User is not active", status=status.HTTP_403_FORBIDDEN)

        if Token.objects.filter(user=u):
            return Response(Token.objects.get(user=u).key)
        return Response(Token.objects.create(user=u).key)


class ServiceListJSON(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response([x.as_dict() for x in models.Service.objects.all()])

class FormTypeListJSON(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        #service = get_object_or_404(models.Service, pk)
        return Response([x.as_dict() for x in models.ServiceForm.objects.all()])

class FormListJSON(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, form_type_id, format=None):
        service_form = get_object_or_404(models.ServiceForm, pk=form_type_id)
        service = service_form.service
        f = forms.RequestForm(service_form=service_form)
        return Response(f.as_dict())

    def post(self, request, form_type_id, format=None):
        service_form = get_object_or_404(models.ServiceForm, pk=form_type_id)
        service = service_form.service
        f = forms.RequestForm(request.POST, service_form=service_form)
        if f.is_valid():
            srf = models.ServiceRequestForm(service=service, form=service_form, requested_by=request.user)
            srf.save(f.cleaned_data)
            return Response(srf.id, status=status.HTTP_201_CREATED)
        return Response(f.as_dict(), status=status.HTTP_400_BAD_REQUEST)


class FormDetailJSON(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, form_type_id, form_id, format=None):
        srf = get_object_or_404(models.ServiceRequestForm, id=form_id)
        return Response(srf.as_dict())


    def post(self, request, form_type_id, form_id, format=None):
        srf = get_object_or_404(models.ServiceRequestForm, id=form_id)
        service_form = srf.form
        service = service_form.service
        f = forms.RequestForm(request.POST, service_form=service_form)
        if f.is_valid():
            srf.save(f.cleaned_data)
            return Response(srf.id, status=status.HTTP_201_CREATED)
        return Response(f.as_dict(), status=status.HTTP_400_BAD_REQUEST)
