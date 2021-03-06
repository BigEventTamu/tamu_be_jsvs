from django.contrib import admin
from job_site_verification.models import *

class FieldsInline(admin.StackedInline):
    model = ServiceFormField
    extra = 2

class ServiceFormAdmin(admin.ModelAdmin):
    inlines = [FieldsInline]

class ChoicesInline(admin.StackedInline):
    model = ServiceFormFieldChoice
    extra = 2


admin.site.register(ServiceRequestForm)
admin.site.register(ServiceRequestFormFieldAnswer)
admin.site.register(ServiceForm, ServiceFormAdmin)
admin.site.register(ServiceFormField)
admin.site.register(JobRequestStub)
admin.site.register(Service)
