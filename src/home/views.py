from django.shortcuts import render, redirect
from django.views.generic import View
from v1.models import Subscriber, Report
from django.conf import settings
import json


class Index(View):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        subs = Subscriber.objects.all()
        reports = reversed(Report.objects.all().order_by('-id')[:5])
        last_update = Report.objects.latest('id')
        context['subscriber'] = subs
        r = Report.objects.exclude(pH_level__isnull=True).exclude(pH_level__exact=0)[:5]
        context['reports'] = r
        context['last_update'] = str(r[0].created_time)

        temperature_level = Report.objects.exclude(temperature_level__isnull=True).exclude(temperature_level__exact=0)
        context['temperature_level'] = temperature_level.latest('created_time').temperature_level
        pH_level = Report.objects.exclude(pH_level__isnull=True).exclude(pH_level__exact=0)
        context['pH_level'] = pH_level.latest('created_time').pH_level
        water_level = Report.objects.exclude(water_level__isnull=True).exclude(water_level__exact='')
        context['water_level'] = water_level.latest('created_time').water_level
        oxygen_level = Report.objects.exclude(oxygen_level__isnull=True).exclude(oxygen_level__exact=0)
        context['oxygen_level'] = oxygen_level.latest('created_time').oxygen_level
        feed_number = Report.objects.exclude(fish_feed_grams__isnull=True).exclude(fish_feed_grams__exact=0)
        context['fish_feed_grams'] = feed_number.latest('created_time').fish_feed_grams
        feeder_grams = Report.objects.exclude(feeder_grams__isnull=True).exclude(feeder_grams__exact=0)
        context['feeder_grams'] = feeder_grams.latest('created_time').feeder_grams
        average_fishes_weight = Report.objects.exclude(average_fishes_weight__isnull=True).exclude(average_fishes_weight__exact=0)
        context['average_fishes_weight'] = average_fishes_weight.latest('created_time').average_fishes_weight
        fish_numbers = Report.objects.exclude(fish_number__isnull=True).exclude(fish_number__exact=0)
        context['fish_number'] = fish_numbers.latest('created_time').fish_number

        context['register_url'] = settings.GLOBE_URL + settings.REGISTER_URL
        context['sms_num'] = settings.SMS_REGISTER_NUM
        context['sms_num_cross_telco'] = settings.SMS_REGISTER_NUM_CROSSTELCO
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        sub_id = request.POST.get('id')
        print sub_id
        sub = Subscriber.objects.get(id=sub_id)
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        role = request.POST.get('role', '')
        print role
        if name:
            sub.name = name
        if address:
            sub.address = address
        if role:
            sub.role = role
        sub.save()
        return redirect('/')
