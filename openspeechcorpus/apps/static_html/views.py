from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Index(TemplateView):
    template_name = 'static_html/index.html'


class Donate(TemplateView):
    template_name = 'static_html/donate.html'


class Download(TemplateView):
    template_name = 'static_html/download.html'


class Learn(TemplateView):
    template_name = 'static_html/learn.html'


class Listen(TemplateView):
    template_name = 'static_html/listen.html'


class Rate(TemplateView):
    template_name = 'static_html/rate.html'