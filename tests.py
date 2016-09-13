from functions import *
import unittest

class TestStringMethods(unittest.TestCase):      
    def atestThreshold(self):
        device = Device.objects.get(name='Fan interior')
        climate = Climate.objects.get(name='Humidity indoor')
        climate.value = 25
        climate.save()
        setDeviceState(device,False)
        control = ClimateControl.objects.get(device=device)
         
        climateControlDevice(control)
        device = Device.objects.get(name='Fan interior')
        self.assertEqual(device.state, str(False))
         
        climate.value = 95
        climate.save()
        control = ClimateControl.objects.get(device=device)
        climateControlDevice(control)
        device = Device.objects.get(name='Fan interior')
        self.assertEqual(device.state, str(True))
         
        climate.value = 89
        climate.save()
        control = ClimateControl.objects.get(device=device)
        climateControlDevice(control)
        device = Device.objects.get(name='Fan interior')
        self.assertEqual(device.state, str(True))
         
        climate.value = 70
        climate.save()
        control = ClimateControl.objects.get(device=device)
        climateControlDevice(control)
        device = Device.objects.get(name='Fan interior')
        self.assertEqual(device.state, str(False))
        
    def atestFunctions(self):
        configureGPIO()
        configureEmail()
        #sendMail(text)
        #updateValues()
        updateClimateIndoor()
        checkLight()
        lightTimerShouldOn(light)
        climateControl()
        #getDeviceState()
        #setDeviceState(device,state)
        checkClimateAlerts()
        sendAlert(alert)
        self.assertTrue(True)
        
    def atestgetPinState(self):
        configureGPIO()
        print(GPIO.input(11))
        
    def testRelay(self):
        configureGPIO()
        print(GPIO.input(12))
        GPIO.output(12,GPIO.LOW)
        print(GPIO.input(12))
        
def main():
    unittest.main()

if __name__ == '__main__':
    main()