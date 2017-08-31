from rest_framework import serializers
from v1.models import Report, Subscriber


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['context', 'pH_level', 'temperature_level', 'water_level',
            'oxygen_level', 'fish_number', 'average_fishes_weight', 'feed_number',
            'feeder_grams']


class SuscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['subscriber_number', 'access_token']
