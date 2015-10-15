from django import forms
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms import widgets

from job_site_verification.models import *

class ChoiceCharRenderer(forms.RadioSelect.renderer):
    def __init__(self, *args, **kwargs):
        super(ChoiceCharRenderer, self).__init__(*args, **kwargs)
        self.choices, self.other = self.choices[:-2], self.choices[-1]

    def __iter__(self):
        count = 0
        for inp in super(ChoiceCharRenderer, self).__iter__():
            count += 1
            yield inp
        _id = '%s_%s' % (self.attrs['id'], count) if 'id' in self.attrs else ""
        label_for = ' for="%s"' % _id if _id else ''
        checked = '' if not force_unicode(self.other[0]) == self.value else 'checked="true" '
        yield '<label%s><input type="radio" id="%s" value="%s" name="%s" %s /> %s </label> %%s' % (label_for, _id, "other", self.name, checked, self.other,)


class ChoiceCharWidget(forms.MultiWidget):
    def __init__(self, choices):
        widgets = [
            forms.RadioSelect(choices=choices, renderer=ChoiceCharRenderer),
            forms.TextInput
        ]
        super(ChoiceCharWidget, self).__init__(widgets)

    def decompress(self, value):
        if not value:
            return [None, None]
        else:
            return value

    def format_output(self, rendered_widgets):
        return rendered_widgets[0]  % rendered_widgets[1]

class ChoiceCharField(forms.MultiValueField):
    def __init__(self, service_form_field, *args, **kwargs):
        choices = [(str(x.pk),x.choice) for x in service_form_field.serviceformfieldchoice_set.all()]
        choices += ("other", "Other, please specify: ")
        fields = [
            forms.ChoiceField(widget=forms.RadioSelect(renderer=ChoiceCharRenderer), *args, **kwargs),
            forms.CharField(required=False)
        ]
        widget = ChoiceCharWidget(choices=choices)
        self._was_required = kwargs.pop('required', True)
        kwargs['required'] = False
        help_text=service_form_field.help_text
        super(ChoiceCharField, self).__init__(*args, widget=widget, fields=fields, label=service_form_field.field_label, help_text=help_text, **kwargs)

    def compress(self, value):
        if self._was_required and not value or value[0] in (None, ''):
            raise forms.ValidationError(self.error_messages['required'])
        if not value:
            return [None, u'']
        return (value[0], value[1] if force_unicode(value[0]) == force_unicode(self.fields[0].choices[-1][0]) else u'')

class UINField(forms.CharField):
    def __init__(self, *args, **kargs):
        super(UINField, self).__init__(*args, **kargs)

class NameToNetIDField(forms.CharField):
    def __init__(self, service_form_field, *args, **kwargs):
        label = service_form_field.field_label
        required = service_form_field.required
        if service_form_field.help_text:
            help_text = service_form_field.help_text
        else:
            help_text = "Enter name and click on correct user. Their netid will popluate the field."
        super(NameToNetIDField, self).__init__(*args,label=label, required=required, help_text=help_text, **kwargs)

class TextField(forms.CharField):
    def __init__(self, service_form_field, *args, **kwargs):
        label = service_form_field.field_label
        required = service_form_field.required
        help_text=service_form_field.help_text
        super(TextField, self).__init__(*args, label=label, help_text=help_text, required=required, widget=forms.Textarea, **kwargs)

class DNSExistsField(forms.CharField):
    def __init__(self, service_form_field, *args, **kwargs):
        label = service_form_field.field_label
        required = service_form_field.required
        help_text=service_form_field.help_text
        super(DNSExistsField, self).__init__(*args, label=label, help_text=help_text, required=required, **kwargs)

class DNSAvailableField(forms.CharField):
    def __init__(self, service_form_field, *args, **kwargs):
        label = service_form_field.field_label
        required = service_form_field.required
        help_text=service_form_field.help_text
        super(DNSAvailableField, self).__init__(*args, label=label, help_text=help_text, required=required, **kwargs)

class ReplyToField(forms.EmailField):
    def __init__(self, service_form_field, *args, **kwargs):
        label = service_form_field.field_label
        required = service_form_field.required
        help_text=service_form_field.help_text
        super(ReplyToField, self).__init__(*args, label=label, help_text=help_text, required=required, **kwargs)
__author__ = 'boredom23309'
