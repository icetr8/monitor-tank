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
        print url
        print resp_json
        return resp_json
