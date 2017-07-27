from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ReportSerializer, SuscriberSerializer
from .models import Report, Subscriber
from .utils import GlobeClient
from django.conf import settings
import ast

globe_client = GlobeClient(settings.GLOBE_URL)
devapi_client = GlobeClient(settings.DEVAPI_URL)


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
                if serializer.is_valid():
                    serializer.save()
                    return HttpResponse("SUCCESFULLY REGISTERED AS SUSBCRIBER")
            return HttpResponse(serializer.errors)
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
        context = request.data['inboundSMSMessageList']['inboundSMSMessage'][0]['message']
        context = '{' + context + '}'
        context_dict = {}
        try:
            context_dict = ast.literal_eval(context)
        except SyntaxError:
            return Response({'error': 'SyntaxError'}, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        data['context'] = context
        data['pH_level'] = context_dict.get('ph', 0)
        data['temperature_level'] = context_dict.get('temp', 0)
        data['oxygen_level'] = context_dict.get('oxygen', 0)
        data['water_level'] = context_dict.get('water', 'normal')

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            subscriber_list = Subscriber.objects.all()
            for subs in subscriber_list:
                devapi_client.send_sms_subscriber(subs.subscriber_number, subs.access_token, context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
