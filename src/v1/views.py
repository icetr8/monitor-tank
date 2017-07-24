from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ReportSerializer, SuscriberSerializer
from .models import Report, Suscriber
from .utils import GlobeClient
from django.conf import settings

globe_client = GlobeClient(settings.GLOBE_URL)


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
            return HttpResponse("TRY TO CONFIRM NUMBER AGAIN")
        return Response({"v1": "Register a user"})

    def post(self, request,):
        serializer = SuscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
