from django.contrib import admin

from .models import *

admin.site.register(Device)
admin.site.register(DeviceTimer)
admin.site.register(Climate)
admin.site.register(ClimateControl)
admin.site.register(ClimateAlert)