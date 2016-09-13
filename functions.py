import sys;sys.path.append(r'/home/pi/greenhouse/pysrc')
import pydevd;
import sqlite3
import random
import os
import django
import RPi.GPIO as GPIO  # # Import GPIO library
import datetime
import time
from datetime import tzinfo
import smtplib  # for email
# import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import inspect #for getting the parent function name. Used for logging purposes
# all the GPIO should be configured at startup

# django setup                    
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greenhouse.settings")
django.setup()
from interface.models import *

#pydevd.settrace("192.168.1.253", stdoutToServer=True, stderrToServer=True) #for debugging

def configureGPIO():
    GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
    devices = Device.objects.all()
    for device in devices:
            GPIO.setup(device.pin, GPIO.OUT)

def configureEmail():
    fromaddr = "mail.alert@email.com"
    toaddr = "lorenzolerate@gmail.com" #Take from DB
    password = "standH1hg"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Python email"
    msg.attach(MIMEText(text, 'plain'))
    # For sending the mail, we have to convert the object to a string, and then use the same prodecure as above to send using the SMTP server..
    server = smtplib.SMTP('smtp.mail.com', 587)

def sendEmail(text):
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    
def updateValues():
    updateClimateIndoor()
    # updateClimateOutdoor()
    # updateCO2

# def checkLight():
  
def updateClimateIndoor():   
    
    # get values from sensor
    # climateIndoor = getClimateIndoor()
    temperatureIndoor = Climate.objects.get(name='Temperature indoor')
    humidityIndoor = Climate.objects.get(name='Humidity indoor')
    
    temperatureIndoor.value = random.randrange(20, 30) #replace getting values from sensor
    humidityIndoor.value = random.randint(0, 100) #replace getting values from sensor
    
    temperatureIndoor.save()
    humidityIndoor.save()
    
    log("Climate indoor update")

def checkLight():
#     log("Checking light")
    # check if the light should be OFF/ON/AUTO
    light = Device.objects.get(name='Light')
    pin = light.pin
    
    if(light.state == 'off'):  # OFF
        GPIO.output(pin, False)
        log("Light OFF")
    elif(light.state == 'on'):  # ON
        GPIO.output(pin, True)
        log("Light ON")
    elif(light.state == 'auto'):  # AUTO
        log("Light AUTO")
        lightTimerShouldOn(light)
    elif(light.state == 'error'):
        raise Exception("Light state = ERROR")
    else:
        raise Exception("Light unknow state. State: " + str(light.state))
        
def lightTimerShouldOn(light):
    timer = DeviceTimer.objects.get(device=light)  # only one timer per light
    currentHour = datetime.datetime.now().time()
    startHour = timer.start_hour
    stopHour = timer.stop_hour
    log(str(currentHour))
    log(str(startHour))
    log(str(stopHour))
    
    if(startHour < stopHour):# it stops before 12am
        if((startHour < currentHour) & (currentHour < stopHour)):
            GPIO.output(light.pin, False)
            log("AutoLight ON1")
        else:
            GPIO.output(light.pin, True)
            log("AutoLight OFF1")
    else:
        if((stopHour < currentHour) & (currentHour < startHour)):
            GPIO.output(light.pin, True)
            log("AutoLight OFF2")
        else:
            GPIO.output(light.pin, False)
            log("AutoLight ON2")
                     
def climateControl():
    # there is a problem with this implementation. The devices could be activated very often for a little time period.
    # solution: add threshold in % or add new values
    # need to control disable devices
    # example of the co2 vs temperature. CO2 is critical while light is ON
    controlsEnabled = climateControl.objects.get(state=True)  # filter by enabled controls
    
    for control in controlsEnabled:
        climateControlDevice(control)
        
def climateControlDevice(control):  #function called by climateControl once for each ClimateControl enabled
    minValue = control.value_min
    maxValue = control.value_max
    climate = control.climate
    threshold = control.threshold
    
    device = control.device
    deviceState = control.device_state  # the state the device should have when reach the threshold
    pin = device.pin
    climateValue = climate.value
    
    if((minValue is None) & (maxValue is None)):
        log("Both values NULL. Do nothing. Check configuration!")
    elif((minValue is not None) & (maxValue is not None)):
        log("Both values NOT NULL. Do nothing. Only once can be NULL. Check configuration!")
    elif(minValue is not None): #from here works if the configuration is correct
        thresholdValue = minValue + minValue * threshold / 100
        if(climateValue < minValue):
            setDeviceState(device, deviceState)
            log("Device: "+str(device)+" | Switch state: "+str(deviceState)+". Cond: "+str(climateValue)+"<"+str(minValue))
        elif(climateValue > thresholdValue):#TEST IT
            setDeviceState(device, not deviceState)
            log("Device: "+str(device)+" | Switch state: "+str(deviceState)+". Cond: "+str(climateValue)+">"+str(thresholdValue))
    elif(maxValue is not None):
        thresholdValue = maxValue - maxValue * threshold/100
        if(climateValue > maxValue):
            setDeviceState(device, deviceState)
            log("Device: "+str(device)+" | Switch tate: "+str(deviceState)+". Cond: "+str(climateValue)+">"+str(maxValue))
        elif(climateValue < thresholdValue):
            setDeviceState(device, not deviceState)
            log("Device: "+str(device)+" | Switch tate: "+str(deviceState)+". Cond: "+str(climateValue)+"<"+str(thresholdValue))
                
def getDeviceState(device, state):
    if(not isinstance(device, Device)):
        log("input type invalid. Device type: " + str(type(device)))
    elif(not isinstance(state, bool)):
        log("state input type invalid. State type: " + str(type(state)))
    else:
        pin = device.pin
        if(state):
            GPIO.output(device.pin, True)
        else:
            GPIO.output(device.pin, False)
        device.state = state
        device.save()
        log(device.name + " SET: " + str(device.state))


def setDeviceState(device, state):
    if(not isinstance(device, Device)):
        log("device input type invalid. Device type: " + str(type(device)))
    elif(not isinstance(state, bool)):
        log("state input type invalid. State type: " + str(type(state)))
    else:
        pin = device.pin
        device.state = state
        if(state):
            GPIO.output(device.pin, True)
        else:
            GPIO.output(device.pin, False)
        device.save()
        log(device.name + " SET: " + str(device.state))
        
def checkClimateAlerts():
    alerts = ClimateAlert.objects.all()
    for alert in alerts:
        climate = alert.climate
        climateValue = climate.value
        minValue = alert.value_min
        maxValue = alert.value_max
        if(climateValue > maxValue | climateValue < minValue):
            sendAlert(alert)

def sendAlert(alert):    #TODO
    if(not isinstance(alert, ClimateAlert)):
        log("alert no valid. Alert type: " + type(alert))
    #else:
        
               
def log(message):
    callerFunction = inspect.stack()[1][3]
    print('LOG [' + callerFunction +']: '+message)
