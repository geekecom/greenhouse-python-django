'''
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
    	"""
    	Return the last five published questions (not including those set to be published in the future).
    	"""
    	return Question.objects.filter( pub_date__lte=timezone.now()    ).order_by('-pub_date')[:5]
'''

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.http import Http404

from django.http import HttpResponse
import datetime

from .models import Device
from interface.models import DeviceTimer, Climate

import RPi.GPIO as GPIO # Import GPIO library
from asyncio.tasks import sleep

GPIO.setmode(GPIO.BOARD)

class IndexView(generic.ListView):
    template_name = 'interface/index.html'
    context_object_name = 'device_list'

    def get_queryset(self):
        return Device.objects.all()[:5]
    

def date_test(self):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def deviceDetail(request, device):
    try:
        d = Device.objects.get(name=device)
    except Device.DoesNotExist:
        raise Http404("Device does not exist")
    return render(request, 'interface/switchDevice.html', {'device': d})

def setDeviceState(request, device, state):
   # try:
        d = Device.objects.get(name=device)
        pin = d.pin
        if(state == "off"):
            d.state = "off"
            setPinState(pin, True)
        elif(state == "on"):
            d.state = "on"
            setPinState(pin, False)
        elif(state == "auto"): #in this case the daemon will be responsible of switching
            d.state = "auto"
        else:
            raise Http404("Incorrect state: " + state)
        d.save()
    # except Device.DoesNotExist:
    #except Exception:
     #   raise Http404("Device does not exist. Name received: " + device)
    # try:
    # except Exception:
    #   raise Http404("Cannot modify the state")
    # return render(request, 'interface/index.html', {'device_list': Device.objects.all()})
        return HttpResponse(d.state)

def setLightSchedule(request, startTime, stopTime):
    lightDeviceTimer = DeviceTimer.objects.get(device=Device.objects.get(name='Light'))
    try:
        lightDeviceTimer.start_hour = startTime
        lightDeviceTimer.stop_hour = stopTime
        lightDeviceTimer.save()
    except Exception:
        raise Http404("Cannot change the schedule")
    return HttpResponse(True)

def getTemperatureIndoor(request):
    temperatureIndoor = Climate.objects.get(name='Temperature indoor').value
    return HttpResponse(temperatureIndoor)

def getTemperatureOutdoor(request):
    temperatureOutdoor = Climate.objects.get(name='Temperature outdoor').value
    return HttpResponse(temperatureOutdoor)

def getHumidityIndoor(request):
    humidityIndoor = Climate.objects.get(name='Humidity indoor').value
    return HttpResponse(humidityIndoor)

def getHumidityOutdoor(request):
    humidityOutdoor = Climate.objects.get(name='Humidity outdoor').value
    return HttpResponse(humidityOutdoor)

def getCO2(request):
    CO2 = Climate.objects.get(name='CO2').value
    return HttpResponse(CO2)

def getLightStartTime(request):
    lightStartTime = DeviceTimer.objects.get(device = Device.objects.get(name='Light')).start_hour
    return HttpResponse(lightStartTime)

def getLightStopTime(request):
    lightStopTime = DeviceTimer.objects.get(device = Device.objects.get(name='Light')).stop_hour
    return HttpResponse(lightStopTime)

#----------------------------------------------
def getPinState(request, pin):
    pin = int(pin)
    try:
        pinState = GPIO.input(pin)
    except RuntimeError:    #in case the GPIO pin is not configured
        GPIO.setup(pin, GPIO.OUT)
        pinState = GPIO.input(pin)
    if(pinState == 1):
        pinState = 'OFF'
    elif(pinState == 0):
        pinState = 'ON'
    else:
        pinState = 'ERROR';
    return HttpResponse(pinState)

def setPinState(pin,state):
    try:
        if(state == False):
            GPIO.output(pin,0)
            return True
        elif(state == True):
            GPIO.output(pin,1)
            return True
        else:
            return 'ERROR [setPinState]: Undefined state'
    except RuntimeError:    #in case the GPIO pin is not configured
        GPIO.setup(pin, GPIO.OUT)
        setPinState(pin, state)