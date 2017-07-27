from rest_framework import serializers
from v1.models import Report, Subscriber


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['context', 'pH_level', 'temperature_level', 'water_level',
            'oxygen_level']


class SuscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['subscriber_number', 'access_token']
