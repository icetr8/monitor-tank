from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import ReportSerializer
from .models import Report
# Create your views here.


class Index(APIView):

    def get(self, request,):
        return Response({"GlobeLabs API Connection version":"v1"})
