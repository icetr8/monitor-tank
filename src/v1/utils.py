from django.conf import settings
from urlparse import urljoin
from functools import wraps
import requests
import decimal
import random


class GlobeClient(object):

    def __init__(self, url):
        self.url = url

    def _request(self, endpoint, method='get', data=None):
        method = method.lower()
        url = urljoin(self.url, endpoint)
        resp = getattr(requests, method)(url, json=data,)
        return resp

    def get_access_token(self, code,):
        url = (settings.TOKEN_URL % (settings.APP_ID, settings.APP_SECRET, code))
        token = self._request(url, method='post')
        token_json = token.json()
        token_json['status_code'] = token.status_code

        return token_json

    def send_sms_subscriber(self, subscriber_num, access_token, message):
        url = (settings.SMS_MT_URL.format(settings.SHORTCODE, access_token))
        data = {"outboundSMSMessageRequest": {
               "senderAddress": settings.SHORTCODE,
               "outboundSMSTextMessage": {"message": str(message)},
               "address": int(subscriber_num)
             }
            }
        resp = requests.post(settings.DEVAPI_URL+url, json=data)
        resp_json = resp.json()
        resp_json['status_code'] = resp.status_code
        return resp_json

    def send_sms_gsm_module(self, gsm_number, access_token, message):
        url = (settings.SMS_MT_URL.format(settings.SHORTCODE, access_token))
        data = {"outboundSMSMessageRequest": {
               "senderAddress": settings.SHORTCODE,
               "outboundSMSTextMessage": {"message": str(message)},
               "address": int(gsm_number)
             }
            }
        resp = requests.post(settings.DEVAPI_URL+url, json=data)
        resp_json = resp.json()
        print resp_json
        resp_json['status_code'] = resp.status_code
        return resp_json

class SMS(object):

    multiplier = 0.05  # 5% of total body mass

    def parse(self, Report):
        temperature_level = Report.objects.exclude(temperature_level__isnull=True).exclude(temperature_level__exact=0)
        temp = temperature_level.latest('created_time').temperature_level
        pH_level = Report.objects.exclude(pH_level__isnull=True).exclude(pH_level__exact=0)
        ph = pH_level.latest('created_time').pH_level
        water_level = Report.objects.exclude(water_level__isnull=True).exclude(water_level__exact='')
        water = water_level.latest('created_time').water_level
        oxygen_level = Report.objects.exclude(oxygen_level__isnull=True).exclude(oxygen_level__exact=0)
        oxygen = oxygen_level.latest('created_time').oxygen_level

        message = "pH level is : " + str(ph)
        

        if ph > 5.5 and ph < 8.5:
            message += " , fairly normal."
        elif ph > 8.5:
            message += " , alkaline may be contaminated check the tank."
        elif ph < 5.5:
            message += " , acidic, now activating the 2nd pump. check the tank."

        message += " Temperature level is : " + str(temp) + " degrees Celsius."

        if water is None:
            water = "normal"
        message += " Water Level is " + water

        return message

    def send_to_module(self, Report):
        fish_numbers = Report.objects.exclude(fish_number__isnull=True).exclude(fish_number__exact=0)
        population = fish_numbers.latest('created_time').fish_number
        average_weights = Report.objects.exclude(average_fishes_weight__isnull=True).exclude(average_fishes_weight__exact=0)
        average_weight = average_weights.latest('created_time').average_fishes_weight
        feeder_grams = Report.objects.exclude(feeder_grams__isnull=True).exclude(feeder_grams__exact=0)
        gram = feeder_grams.latest('created_time').feeder_grams

        feed = self.multiplier * (average_weight * population)
        feed_times_result = int(round(feed / gram, 0))
        report = Report.objects.latest('id')
        report.feed_number = feed_times_result
        report.fish_feed_grams = feed

        report.save()

        return feed_times_result
