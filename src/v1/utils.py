from django.conf import settings
from urlparse import urljoin
from functools import wraps
import requests


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


class SMS(object):

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
            message += " ,fairly normal."
        elif ph > 8.5:
            message += " ,alkaline may be contaminated check the tank."
        elif ph < 5.5:
            message += " ,acidic, now activating the 2nd pump. check the tank."

        message += " Temperature level is : " + str(temp) + " degrees Celsius."

        message += " Water Level is " + water

        return message
