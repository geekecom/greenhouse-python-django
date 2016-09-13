from django.db import models
from django.template.defaultfilters import default


class Device(models.Model):
        
    DEVICE_STATE = (
        ('off', 'off'),
        ('on', 'on'),
        ('auto', 'auto'),
        ('ERROR', 'ERROR'))
    
    GPIO_PIN = (
        (7, 7),
        (11, 11),
        (12, 12),
        (13, 13),
        (15, 15),
        (16, 16),
        (18, 18),
        (22, 22),
        (29, 29),
        (31, 31),
        (32, 32),
        (33, 33),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
        (40, 40)
        )
    
    name = models.CharField(max_length=20, unique=True)
    state = models.CharField(max_length=5, choices=DEVICE_STATE)
    pin = models.PositiveSmallIntegerField(choices=GPIO_PIN)
    
    def __str__(self):
        return self.name + ' : ' + str(self.state) + '  | Pin: ' + str(self.pin)
    
class DeviceTimer(models.Model):
    device = models.OneToOneField(Device,
        on_delete=models.CASCADE,
    )
    state = models.BooleanField(default=True)
    start_hour = models.TimeField()
    stop_hour = models.TimeField()
    
    def __str__(self):
        return 'Device: ' + str(self.device.name) + '. Status: ' + str(self.state) + '. Start hour: ' + str(self.start_hour) + ',  Stop hour: ' + str(self.stop_hour)

class Climate(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    pin = models.PositiveSmallIntegerField(default=40)
    
    def __str__(self):
        return self.name + ' : ' + str(self.value)
    
class ClimateControl(models.Model):
    
    THRESHOLD = ((1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
        (39, 39),
        (40, 40),
        (41, 41),
        (42, 42),
        (43, 43),
        (44, 44),
        (45, 45),
        (46, 46),
        (47, 47),
        (48, 48),
        (49, 49),
        (50, 50)
    )
                 
    device = models.ForeignKey(Device,
        on_delete=models.CASCADE,
        )
    climate = models.ForeignKey(Climate,
        on_delete=models.CASCADE,
        )
    state = models.BooleanField(default=True)
    value_min = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    value_max = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    device_state = models.BooleanField(default=False)
    threshold = models.SmallIntegerField(choices=THRESHOLD, default=5)
    
    def __str__(self):
        return self.climate.name + '. ' + self.device.name
    
class ClimateAlert(models.Model):
    climate = models.OneToOneField(Climate,
        on_delete=models.CASCADE,
        )
    state = models.BooleanField(default=True)
    value_min = models.IntegerField(null=True)
    value_max = models.IntegerField(null=True)
    # typeOfAlert
    def __str__(self):
        return self.climate.name + ". min: " + str(self.value_min) + ", max: " + str(self.value_max) + ". State alert: " + str(self.state)

class Configuration(models.Model):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
