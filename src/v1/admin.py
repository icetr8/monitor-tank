from django.contrib import admin
from .models import Report, Suscriber
# Register your models here.


class SuscriberAdmin(admin.ModelAdmin):
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

            )
    list_filter = (
            'created_time',
            'id',
            'pH_level',
            'temperature_level',
            'water_level',
            'oxygen_level',
           )
    search_fields = (
            )
    readonly_fields = (
            'context',
            )


admin.site.register(Suscriber, SuscriberAdmin)
admin.site.register(Report, ReportAdmin)
