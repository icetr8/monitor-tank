from django.shortcuts import render
from django.views.generic import View
from v1.models import Subscriber, Report


class Index(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        subs = Subscriber.objects.all()
        reports = reversed(Report.objects.all().order_by('-id')[:10])
        context['subscriber'] = subs
        context['reports'] = reports
        return render(request, self.template_name, context)
