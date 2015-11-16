import subprocess

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.forms.models import inlineformset_factory

from job_site_verification.models import *
from job_site_verification import fields

class SelectServiceForm(forms.Form):
    service_id = forms.ChoiceField(label="Select Service to Edit")

    def __init__(self, *args, **kwargs):
        super(SelectServiceForm, self).__init__(*args, **kwargs)
        self.fields['service_id'].choices = [(x.pk, x.name) for x in Service.objects.all()]

class ModifyServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description",]


class ModifyRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceForm
        fields = ['name', 'description', 'is_current']

class ModifyServiceFormField(forms.ModelForm):
    class Meta:
        model = ServiceFormField
        fields=['field_label','field_type','help_text', 'required', 'position']

FieldFormSet = inlineformset_factory(ServiceForm, ServiceFormField, form=ModifyServiceFormField, can_order=True, can_delete=True)
ChoiceFormSet = inlineformset_factory(ServiceFormField, ServiceFormFieldChoice,
                                      fields=['choice'], can_delete=True)

class SelectRequestForm(forms.Form):
    service_form_id = forms.ChoiceField()

    def clean(self):
        super(SelectRequestForm, self ).clean()
        service_id, form_id = self.cleaned_data['service_form_id'].split('_')
        try:
            Service.objects.get(pk=int(service_id))
        except ObjectDoesNotExist:
            self._errors["service_form_id"] = "Could not find service. "
        else:
            self.cleaned_data['service_id'] = int(service_id)
        try:
            ServiceForm.objects.get(pk=int(form_id))
        except:
            if self._errors['service_form_id']:
                self._errors['service_form_id'] += " Could not find form. "
            else:
                self._errors['service_form_id'] = " Could not find form. "
        else:
            self.cleaned_data['form_id'] = int(form_id)

        if self._errors:
            del(self.cleaned_data['service_form_id'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(SelectRequestForm, self).__init__(*args, **kwargs)
        choices = []
        for service in Service.objects.all():
            for form in service.serviceform_set.all():
                choices.append(("%i_%i" % (service.pk, form.pk), form.name))
        self.fields['service_form_id'].choices = choices

    
SPECIAL_FIELDS = ('NameToNetIDField')
class RequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        service_form = kwargs.get('service_form')
        if service_form:
            del(kwargs['service_form'])

        super(RequestForm, self).__init__(*args, **kwargs)
        if isinstance(service_form, int):
            service_form = ServiceForm.objects.get(id=service_form)

        if isinstance(service_form, ServiceForm):
            self._service_form = service_form
            for field in service_form.serviceformfield_set.all().order_by('position'):
                if hasattr(forms, field.field_type):
                    if field.help_text:
                        self.fields[field.field_id] = getattr(forms, field.field_type)(label=field.field_label, required=field.required, help_text=field.help_text)
                    else:
                        self.fields[field.field_id] = getattr(forms, field.field_type)(label=field.field_label, required=field.required)
                    if field.serviceformfieldchoice_set.all():
                        choices = []
                        for choice in field.serviceformfieldchoice_set.all():
                            choices.append((str(choice.pk), choice.choice))
                        self.fields[field.field_id].choices = choices
                elif hasattr(fields, field.field_type):
                    self.fields[field.field_id] = getattr(fields, field.field_type)(field)
                else:
                    raise ValueError("Unrecognized field type: %s" % field.field_type)
            self.special_fields = [(x.field_id, x.field_type) for x in service_form.serviceformfield_set.all() if x.field_type in SPECIAL_FIELDS]
        elif isinstance(service_form, ServiceRequestForm):
            raise NotImplementedError("Not able to initialize form from ServiceRequestFormObject")

    def as_dict(self):
        form = {}
        form['form_type'] = self._service_form.id
        form['form_name'] = self._service_form.name
        form['form_desc'] = self._service_form.description
        form['errors'] = self.errors
        form['fields'] = []
        for (id, field_obj) in self.fields.iteritems():
            field = {}
            field['id'] = id
            field['name'] = field_obj.label
            field['type'] = field_obj.__class__.__name__
            field['required'] = field_obj.required
            field['help_text'] = field_obj.help_text
            field['value'] = field_obj.initial
            if hasattr(field_obj, "choices"):
                field['choices'] = [{"id": x[0],"value": x[1]} for x in field_obj.choices]
            if id in self.errors:
                field['errors'] = self.errors[id]
            form['fields'].append(field)
        return form
    
    def clean(self):
        cleaned_data = super(RequestForm, self).clean()
        for field in self._service_form.serviceformfield_set.all():
            if field.field_type == "ChoiceCharField":
                if not self.data.get(field.field_id + "_0") and field.required:
                    self._errors[field.field_id+"_0"] = self.error_class(['An option must be selected'])
                else:
                    del(self._errors[field.field_id])
                    selected = self.data.get(field.field_id + "_0")
                    if selected == "other":
                        cleaned_data[field.field_id] = "Other: " + self.data.get(field.field_id + "_1")
                    else:
                        selected = int(selected)
                        cleaned_data[field.field_id] = field.serviceformfieldchoice_set.get(pk=int(self.data.get(field.field_id + "_0"))).choice
                pass
            elif field.serviceformfieldchoice_set.all():
                if cleaned_data.get(field.field_id):
                    cleaned_data[field.field_id] = field.serviceformfieldchoice_set.get(pk=int(cleaned_data[field.field_id])).choice

        self.cleaned_data = cleaned_data
        #TODO Replace _error labels with field names.
        return self.cleaned_data
