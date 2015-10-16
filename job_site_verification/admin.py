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

class FieldAdmin(admin.ModelAdmin):
    inlines = [ChoicesInline]

admin.site.register(ServiceRequestForm)
admin.site.register(ServiceRequestFormFieldAnswer)
admin.site.register(ServiceForm, ServiceFormAdmin)
admin.site.register(ServiceFormField, FieldAdmin)
admin.site.register(Service)
