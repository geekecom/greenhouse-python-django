from interface.models import Device
from rest_framework import serializers


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'state', 'pin')