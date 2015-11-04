from django.db import models
from django import forms
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string


JOB_STATE_CHOICES = (
    ("survey_canceled", "Survey Canceled"),
    ("needs_survey", "Needs Survey"),
    ("survey_completed", "Survey Completed")
)

class JobRequestStub(models.Model):
    reserved_by = models.ForeignKey(User, blank=True, null=True)
    job_zone = models.CharField(max_length=4, db_index=True)
    job_zone_team = models.CharField(max_length=4, db_index=True)
    job_request_id = models.CharField(max_length=16, db_index=True)
    job_description = models.TextField(max_length=2048)
    job_state = models.CharField(max_length=32, choices=JOB_STATE_CHOICES, default="needs_survey", db_index=True)

    address_1 = models.CharField(max_length="128", blank=True, null=True)
    address_2 = models.CharField(max_length="128", blank=True, null=True)
    zip_code = models.CharField(max_length="16", blank=True, null=True)
    city = models.CharField(max_length="128", blank=True, null=True)
    state = models.CharField(max_length="16", blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __unicode__(self):
        return str(self.job_request_id) + " -- " + self.address()

    def address(self):
        if self.address_1 and self.city and self.state and self.zip_code:
            return "{0} {1}, {2}, {3} {4}".format(self.address_1, self.address_2, self.city, self.state, self.zip_code)
        return ""

    def as_dict(self):
        return {
            "job_request_id": self.job_request_id,
            "job_description": self.job_description,
            "job_state": self.job_state,
            "location":
                {
                    "full_address": self.address,
                    "address_1": self.address_1,
                    "address_2": self.address_2,
                    "zip_code": self.zip_code,
                    "city": self.city,
                    "state": self.state,
                    "lat": self.lat,
                    "lon": self.lon,
                }
        }


class Service(models.Model):
    name = models.CharField(max_length=100, help_text="Name of Service")
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
        return {"name": self.field_label, "type": self.field_type, "id": self.id,
                "help_text": self.help_text, "required": self.required,
                "choices": [{"id": x.id, "value": x.choice} for x in self.serviceformfieldchoice_set.all()]
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
    job_stub = models.ForeignKey(JobRequestStub, blank=True, null=True)
    requested_by = models.ForeignKey(User, blank=True, null=True)
    completed = models.DateTimeField(auto_now=True, editable=False)

    def as_dict(self):
        form = dict()
        form['id'] = self.id
        form['form_type'] = self.form.id
        form['form_name'] = self.form.name
        form['form_desc'] = self.form.description
        if self.job_stub:
            form['job_request'] = self.job_stub.as_dict()
        form['fields'] = []

        field_objs = self.form.serviceformfield_set.all()
        for f in field_objs:
            field_as_dict = f.as_dict()
            if ServiceRequestFormFieldAnswer.objects.filter(form=self, field=f):
                field_as_dict['value'] = ServiceRequestFormFieldAnswer.objects.filter(form=self, field=f).get().answer
            else:
                field_as_dict['value'] = None
            form['fields'].append(field_as_dict)
        return form

    def __unicode__(self):
        return "%s - %s for %s" % (self.service, self.form, self.requested_by)


    def save(self, data, *args, **kwargs):
        super(ServiceRequestForm, self).save(*args, **kwargs)
        for field_id, value in data.iteritems():
            answer_query = self.servicerequestformfieldanswer_set.filter(field_id=field_id)
            if answer_query:
                answer = answer_query.get()
                answer.answer = value
                answer.save()
            else:
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
