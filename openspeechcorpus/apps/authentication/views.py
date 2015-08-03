# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template.context import Context


from .forms import UserForm, User
from .models import ActivationToken

from hashlib import sha1
from random import random
from datetime import datetime, timedelta
# Create your views here.
class SignUp(TemplateView):
    template_name = 'authentication/sign-up.html'
    userform = UserForm(prefix='user')
    userformerrors = None

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        print context
        if 'userform' not in context:
            context['userform'] = self.userform
        if 'userformerrors' not in context:
            context['userformerrors'] = self.userformerrors
        return context

    def post(self, request, *args, **kwargs):
        userform = UserForm(request.POST, prefix='user')
        if userform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            username = userform.cleaned_data['username']
            email = userform.cleaned_data['email']
            salt = sha1(str(random())).hexdigest()[:5]
            activation_key = sha1(salt+email).hexdigest()
            key_expires = datetime.today() + timedelta(2)

            #Get user by username
            user = User.objects.get(username=username)

            # Create and save user profile
            activation_token = ActivationToken(user=user, activation_token=activation_key, expiration=key_expires)
            activation_token.save()

            # Send email with activation key

            context = {
                'url': "http://openspeechcorpus.com/auth/sign-up-confirm/%s" % activation_key
            }

            email_subject = 'Account created successfully'
            email_body = "To activate your account, visit this link: " \
                         "http://openspeechcorpus.com/auth/sign-up-confirm/%s" \
                         % activation_key

            template = get_template('authentication/email-signup-confirmation.html')


            send_mail(
                email_subject,
                email_body,
                'ma0@contraslash.com',
                [email],
                fail_silently=False,
                html_message=template.render(context))
            # return reverse_lazy('index')
        self.userformerrors = userform.errors
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return render(request, self.template_name, self.get_context_data(**kwargs))


class SignUpConfirm(TemplateView):
    template_name = 'authentication/sign-up-confirm.html'

    def get(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            HttpResponseRedirect(reverse_lazy('index'))
        try:
            activation_token = ActivationToken.objects.get(activation_token=self.kwargs['token'])
        except ActivationToken.DoesNotExist:
            return render(
                request,
                self.template_name,
                {
                    'status': _('Invalid URL')
                }
            )

        if activation_token.expiration < timezone.now():
            return render(
                request,
                self.template_name,
                {
                    'status': _('Expired URL')
                }
            )

        user = activation_token.user
        user.is_active = True
        user.save()
        return render(
            request,
            self.template_name,
            {
                'status': _('Your account has been activated, please log in')
            }
        )
