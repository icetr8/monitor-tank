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
    pass

admin.site.register(Suscriber, SuscriberAdmin)
admin.site.register(Report, ReportAdmin)
