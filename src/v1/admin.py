from django.contrib import admin
from .models import Report, Subscriber, CommandLog
# Register your models here.


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'subscriber_number',
            'name',
            'address',
            'role',
            'access_token',
            )
    list_filter = (
            'id',
            'subscriber_number',
            'name',
            'address',
            'role',
            'access_token'
           )
    search_fields = (
            )
    readonly_fields = (
            )


class ReportAdmin(admin.ModelAdmin):
    list_display = (
            'created_time',
            'id',
            'pH_level',
            'temperature_level',
            'water_level',
            'oxygen_level',
            'fish_number',
            'average_fishes_weight',
            'fish_feed_grams',
            'feeder_grams',
            'feed_number'
            )
    list_filter = (
            'created_time',
           )
    search_fields = (
            )
    readonly_fields = (
            'context',
            )


class LogsAdmin(admin.ModelAdmin):
    list_display = (
            'reporter',
            'command'
            )
    list_filter = (
            'reporter',
           )
    search_fields = (
            )
    readonly_fields = (
            )


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(CommandLog, LogsAdmin)
