from django.conf.urls import url

from . import views

# app_name = 'interface'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^date/', views.date_test),  # for testing
   
    url(r'^setDeviceState/(?P<device>\w+)/(?P<state>\w+)/$', views.setDeviceState),
    url(r'^setDeviceState/(?P<device>\w+\s+\w+)/(?P<state>\w+)/$', views.setDeviceState),
    url(r'^setLightSchedule/(?P<startTime>[0-9]{2}\:[0-9]{2})/(?P<stopTime>[0-9]{2}\:[0-9]{2})', views.setLightSchedule),
    
    url(r'^getTemperatureIndoor/', views.getTemperatureIndoor),
    url(r'^getTemperatureOutdoor', views.getTemperatureOutdoor),
    url(r'^getHumidityIndoor', views.getHumidityIndoor),
    url(r'^getHumidityOutdoor', views.getHumidityOutdoor),
    url(r'^getCO2', views.getCO2),
    url(r'^getLightStartTime', views.getLightStartTime),
    url(r'^getLightStopTime', views.getLightStopTime),
    
    url(r'^getPinState/(?P<pin>[0-9]+)', views.getPinState),
]
