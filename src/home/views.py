from django.shortcuts import render
from django.views.generic import View
from v1.models import Subscriber, Report
from django.conf import settings
import json


class Index(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        subs = Subscriber.objects.all()
        reports = reversed(Report.objects.all().order_by('-id')[:10])
        last_update = Report.objects.latest('id')
        context['subscriber'] = subs
        context['reports'] = reports
        context['last_update'] = str(last_update.created_time)

        temperature_level = Report.objects.exclude(temperature_level__isnull=True).exclude(temperature_level__exact=0)
        context['temperature_level'] = temperature_level.latest('created_time').temperature_level
        pH_level = Report.objects.exclude(pH_level__isnull=True).exclude(pH_level__exact=0)
        context['pH_level'] = pH_level.latest('created_time').pH_level
        water_level = Report.objects.exclude(water_level__isnull=True).exclude(water_level__exact='')
        context['water_level'] = water_level.latest('created_time').water_level
        oxygen_level = Report.objects.exclude(oxygen_level__isnull=True).exclude(oxygen_level__exact=0)
        context['oxygen_level'] = oxygen_level.latest('created_time').oxygen_level

        context['register_url'] = settings.GLOBE_URL + settings.REGISTER_URL
        context['sms_num'] = settings.SMS_REGISTER_NUM
        context['sms_num_cross_telco'] = settings.SMS_REGISTER_NUM_CROSSTELCO
        return render(request, self.template_name, context)
