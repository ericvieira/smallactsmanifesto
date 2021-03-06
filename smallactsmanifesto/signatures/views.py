# coding: utf-8
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse as r
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import DetailView
from .forms import SignupForm
from .models import Signatory


class SignupView(CreateView):
    "Shows the signup form and saves it's submission."
    form_class = SignupForm
    template_name = 'signatures/signup_form.html'
    template_email_subject = 'signatures/signup_email_subject.txt'
    template_email_body = 'signatures/signup_email_body.txt'

    def get_success_url(self):
        return r('signatures:success')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        self.send_confirmation_email()
        return response

    def send_confirmation_email(self):
        """
        Sends the signup confirmation email to the Signatory.
        He will only be listed after access the confirmation link.
        """
        context = { 'object': self.object }
        subject = render_to_string(self.template_email_subject, context)
        message = render_to_string(self.template_email_body, context)

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
                  [self.object.email, settings.DEFAULT_FROM_EMAIL])


class SignupSuccessView(TemplateView):
    'Shows a success page after user has signedup.'
    template_name='signatures/signup_success.html'


class ConfirmView(DetailView):
    template_name = 'signatures/signup_confirm.html'
    slug_field = 'confirmation_key'
    model = Signatory

    def get_object(self, queryset=None):
        'Load and update Signatory active status.'
        obj = super(ConfirmView, self).get_object(queryset)

        obj.is_active = True
        obj.save()
        return obj
