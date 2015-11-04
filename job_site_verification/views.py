from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.middleware import csrf
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
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
            Token.objects.get(user=u).delete()
        return Response(Token.objects.create(user=u).key)


class ServiceListJSON(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response([x.as_dict() for x in models.Service.objects.all()])

class JobStubListJSON(APIView):

    def get(self, request):
        job_state = request.GET.get("job_state", "needs_survey")
        job_zone = request.GET.get("job_zone")
        job_zone_team = request.GET.get('job_zone_team')

        if not job_state in [x[0] for x in models.JOB_STATE_CHOICES]:
            return Response("{0} is not a valid job_state".format(job_state))
        page = None
        if 'page' in request.GET:
            try:
                page = request.GET['page']
            except PageNotAnInteger:
                return Response({"error":"Page number provideds is not an integer"}, status=status.HTTP_400_BAD_REQUEST)
        page = page or 1
        jrs = models.JobRequestStub.objects.filter(job_state=job_state)
        if job_zone:
            jrs.filter(job_zone=job_zone)
        if job_zone_team:
            jrs.filter(job_zone_team=job_zone_team)
        paginator = Paginator(jrs, 50)
        data = dict()
        data['current_page'] = page
        data["job_state"] = job_state
        data["num_pages"] = paginator.num_pages
        try:
            data["job_stubs"] = [x.as_dict() for x in paginator.page(page)]
        except EmptyPage:
            data['job_stubs'] = []
        return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)




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
        job_request_id  = request.POST.get("job_request_id")
        if not job_request_id :
            return Response("job_request_id is required.", status=status.HTTP_400_BAD_REQUEST)
        job_request = get_object_or_404(models.JobRequestStub, job_request_id=job_request_id)
        f = forms.RequestForm(request.POST, service_form=service_form)
        if f.is_valid():
            job_request.job_state = "survey_completed"
            job_request.save()
            srf = models.ServiceRequestForm(service=service, form=service_form, requested_by=request.user,
                                            job_stub=job_request)
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


class FormTypeList(View):
    def get(self, request):
        form_types_list = models.ServiceForm.objects.all()
        return render(request, "form_edit/form_list.html", {"form_types": form_types_list})


class Index(View):
    @method_decorator(login_required)
    def get(self, request):
        stats = {}
        stats["need_survey"] = models.JobRequestStub.objects.filter(job_state="needs_survey").count()
        stats["surveys_completed"] = models.JobRequestStub.objects.filter(job_state="survey_completed").count()
        return render(request, "index.html", {"stats": stats})