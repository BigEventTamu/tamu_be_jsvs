from django.db import models
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string

class Service(models.Model):
    name = models.CharField(max_length=100,help_text="Name of Service")
    description = models.TextField(help_text="Description of Service")

    def __unicode__(self):
        return self.name

    def as_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class ServiceForm(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()
    service = models.ForeignKey(Service,help_text="Which service is this form for?")
    is_current = models.BooleanField(help_text="Is available for customer to complete", default=True)

    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "is_current": self.is_current
        }

    def __unicode__(self):
        return self.name

FIELD_TYPE_CHOICES = (
    ('CharField', 'Character Field'),
    ('TextField', 'Open Ended Text Field'),
    ('BooleanField', 'Boolean Field'),
    ('ChoiceField', 'Choice Field'),
    ('ChoiceCharField', 'Choice Field with "Other" prompt'),
    ('EmailField', 'Email Address Field'),
    ('IntegerField', 'Integer Field'),
)

class ServiceFormField(models.Model):
    field_label = models.CharField("Prompt", max_length=150, help_text="Ex: How many accounts?")
    field_type = models.CharField(choices=FIELD_TYPE_CHOICES,max_length=32,)
    form = models.ForeignKey(ServiceForm)
    help_text = models.CharField(max_length=150,help_text="Help text looks like this. May leave blank", null=True,blank=True)
    position = models.IntegerField(blank=True,default=1000)
    required = models.BooleanField(default=True, help_text="Can user leave this field blank?")

    class META:
        ordering = ['position']

    def as_dict(self):
        return {"field_label": self.field_label, "field_type": self.field_type, "form": self.form.as_dict(),
                "help_text": self.help_text, "position": self.position, "required": self.required,
                "choices":[x.choice for x in self.serviceformfieldchoice_set.all()]
                }


    @property
    def field_id(self):
        return str(self.pk)

    def save(self):
        if not self.position or self.position == 1000:
            self.position = self.form.serviceformfield_set.order_by('-position')[0].position + 1 if self.form.serviceformfield_set.all() else 1
        super(ServiceFormField, self).save()

    def __unicode__(self):
        return "%s - %s" % (self.field_label, self.field_type)

    #def serviceformfield_set(self, *args, **kwargs):
    #    return super(ServiceFormField, self).serviceformfield_set(*args, **kwargs).order_by('-position')

class ServiceFormFieldChoice(models.Model):
    choice = models.CharField(max_length=128)
    field = models.ForeignKey(ServiceFormField)

    def as_dict(self):
        pass

    def __unicode__(self):
        return "%s: %s" % (self.field.field_label, self.choice) 

class ServiceRequestForm(models.Model): #One per customer per service request
    service = models.ForeignKey(Service)
    form = models.ForeignKey(ServiceForm)
    requested_by = models.ForeignKey(User, blank=True, null=True)
    completed = models.DateTimeField(auto_now=True, editable=False)

    def as_dict(self):
        rf = {
            "service": self.service.as_dict(),
            "form": self.form.as_dict(),
            "fields": []
        }
        field_objs = self.form.serviceformfield_set.all()
        for f in field_objs:
            field_as_dict = f.as_dict()
            if ServiceRequestFormFieldAnswer.objects.filter(form=self, field=f):
                field_as_dict['value'] = ServiceRequestFormFieldAnswer.objects.filter(form=self, field=f).get().answer
            else:
                field_as_dict['value'] = None
            rf['fields'].append(field_as_dict)
        return rf

    def __unicode__(self):
        return "%s - %s for %s" % (self.service, self.form, self.requested_by)


    def save(self, data, *args, **kwargs):
        super(ServiceRequestForm, self).save(*args, **kwargs)
        for field_id, value in data.iteritems():
            answer = ServiceRequestFormFieldAnswer(form=self, field=ServiceFormField.objects.get(pk=field_id), answer=value)
            answer.save()
        return self

    def send_message(self):
        send_to = [self.service.send_to]
        reply_to = "no-reply@boredom23309-dev.cis.tamu.edu"
        for answer in self.servicerequestformfieldanswer_set.all():
            field = ServiceFormField.objects.get(pk=answer.field.pk)
            if field.field_type == "ReplyToField":
                reply_to = answer.answer
        message = render_to_string('request_form/completed_form.eml', {"service_request_form":self})
        subject = self.__unicode__()
        send_mail(subject, message, reply_to, send_to)

class ServiceRequestFormFieldAnswer(models.Model): #One per field per cutomer per service request. 
    form = models.ForeignKey(ServiceRequestForm)
    field = models.ForeignKey(ServiceFormField)
    answer = models.TextField()

    def as_dict(self):
        pass


    def __unicode__(self):
        return "%s - %s : %s" % (self.form.form.name, self.field.field_label, self.answer)
