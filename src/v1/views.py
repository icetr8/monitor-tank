from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import ReportSerializer, SuscriberSerializer
from .models import Report, Suscriber
# Create your views here.


class Index(APIView):

    def get(self, request,):
        return Response({"GlobeLabs API Connection version": "v1"})


class Suscriber(APIView):
    def get(self, request,):
        return Response({"v1": "Register a user"})

    def post(self, request,):
        print request.data
        serializer = SuscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
