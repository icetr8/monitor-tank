from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ReportSerializer, SuscriberSerializer
from .models import Report, Subscriber, CommandLog, ManualCommandLog
from .utils import GlobeClient, SMS
from django.conf import settings
import ast
import random

globe_client = GlobeClient(settings.GLOBE_URL)
devapi_client = GlobeClient(settings.DEVAPI_URL)
sms = SMS()


class Index(APIView):

    def get(self, request,):
        return Response({"GlobeLabs API Connection version": "v1"})


class Suscriber(APIView):
    def get(self, request,):
        if request.GET.get('code', ''):
            code = request.GET.get('code', '')
            token = globe_client.get_access_token(code)
            access_token = token.get('access_token', '')
            subscriber_number = token.get('subscriber_number', '')
            if access_token and subscriber_number:
                token.pop('status_code')
                serializer = SuscriberSerializer(data=token)
                existing = Subscriber.objects.all().filter(subscriber_number=subscriber_number)
                if existing:
                    existing[0].access_token = access_token
                    existing[0].save()
                    return HttpResponse("UPDATED SUSBCRIBER")
                if serializer.is_valid():
                    serializer.save()
                    return HttpResponse("SUCCESFULLY REGISTERED AS SUSBCRIBER")
                return Response(serializer.errors)
            return HttpResponse("wrong code")
        return Response({"v1": "Register a user"})

    def post(self, request,):
        serializer = SuscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SMSRECIEVER(APIView):
    def get(self, request,):
        return Response({"v1": "SMS Reciever"})

    def post(self, request,):
        try:
            data = request.data['manual']
            gsm = Subscriber.objects.filter(name="SMS_MODULE")[0]
            devapi_client.send_sms_gsm_module(gsm.subscriber_number, gsm.access_token, str(data))
            cmd = ManualCommandLog(reporter=gsm, command=data, web=True)
            cmd.save()
            return Response({'manual': data})
        except KeyError:
            pass
        web = None
        try:
            web = request.data['inboundSMSMessageList[inboundSMSMessage][0][message]']
        except KeyError:
            pass
        if web:
            context_msg = request.data['inboundSMSMessageList[inboundSMSMessage][0][message]']
        else:
            context_msg = request.data['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
        context = '{' + context_msg + '}'
        context_dict = {}
        try:
            context_dict = ast.literal_eval(context)
        except SyntaxError:
            return Response({'error': 'SyntaxError'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            data = str(context_msg)
            msg = ""
            msg_subs = 'You have texted '
            if 'feed' == context_msg.lower():
                msg = 'feed'
                msg_subs += msg
            elif 'status' == context_msg.lower():
                msg = 'status'
                msg_subs += msg
            elif 'pump' == context_msg.lower():
                msg = 'pump'
                msg_subs += msg
            elif 'once' == context_msg.lower():
                msg = 'once'
                msg_subs += msg
            elif 'twice' == context_msg.lower():
                msg = 'twice'
                msg_subs += msg
            elif 'support' == context_msg.lower():
                msg_subs = 'feed = pour feeds to fishes \npump = pump water \n' \
                'status = update subscribers pH, temp and water level \n' \
                'once = once feeding per day \ntwice = twice feeding per day'
            elif 'ask' == context_msg.lower():
                gsm = Subscriber.objects.filter(name="SMS_MODULE")[0]
                feed_num = Report.objects.exclude(feed_number__isnull=True)
                feed = feed_num.latest('created_time').feed_number
                import time
                time.sleep(30)
                devapi_client.send_sms_gsm_module(gsm.subscriber_number, gsm.access_token, str(feed))
                cmd = ManualCommandLog(reporter=gsm, command='ask')
                cmd.save()
                return Response({'ask': 'true'})
            else:
                msg_subs = 'You have texted an invalid command. Might be mispelled \n \n'\
                    'feed = pour feeds to fishes \npump = pump water \n' \
                    'status = update subscribers pH, temp and water level \n' \
                    'once = once feeding per day \ntwice = twice feeding per day'
            if msg:
                gsm = Subscriber.objects.filter(name="SMS_MODULE")[0]
                devapi_client.send_sms_gsm_module(gsm.subscriber_number, gsm.access_token, msg)

            num = request.data['inboundSMSMessageList']['inboundSMSMessage'][0]['senderAddress']
            number = num.replace("tel:+63", "")

            subs = Subscriber.objects.filter(subscriber_number=number)[0]
            if subs.name != 'SMS_MODULE':
                devapi_client.send_sms_gsm_module(subs.subscriber_number, subs.access_token, str(msg_subs))
            cmd = ManualCommandLog(reporter=subs, command=msg)
            cmd.save()
            return Response({'data': msg})
        data = {}
        data['context'] = context
        data['pH_level'] = context_dict.get('ph', 0)
        data['temperature_level'] = context_dict.get('temp', 0)
        data['oxygen_level'] = context_dict.get('oxygen', 0)
        data['water_level'] = context_dict.get('water', '')
        data['fish_number'] = context_dict.get('population', )
        data['average_fishes_weight'] = context_dict.get('weight', )
        data['fish_feed_grams'] = context_dict.get('feed', )
        data['feed_number'] = context_dict.get('number', )
        data['feeder_grams'] = context_dict.get('grams',)

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            subscriber_list = Subscriber.objects.all()
            if data['fish_feed_grams']:
                fish_feed_grams = data['fish_feed_grams']
                gsm = Subscriber.objects.filter(name="SMS_MODULE")[0]
                feeder_grams = Report.objects.exclude(feeder_grams__isnull=True).exclude(feeder_grams__exact=0)
                gram = feeder_grams.latest('created_time').feeder_grams
                feed_times_result = int(round(float(fish_feed_grams) / gram, 0))
                report = Report(fish_feed_grams=float(fish_feed_grams), feed_number=feed_times_result)
                report.save()
                devapi_client.send_sms_gsm_module(gsm.subscriber_number, gsm.access_token, str(feed_times_result))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            if data['pH_level']:
                message = sms.parse(Report)
                for subs in subscriber_list:
                    if subs.name != 'SMS_MODULE':
                        msg = "Hello " + subs.name + ". " + message
                        devapi_client.send_sms_subscriber(subs.subscriber_number, subs.access_token, msg)
            else:
                module_message = sms.send_to_module(Report)
                gsm = Subscriber.objects.filter(name="SMS_MODULE")[0]
                devapi_client.send_sms_gsm_module(gsm.subscriber_number, gsm.access_token, str(module_message))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
