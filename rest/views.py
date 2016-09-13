from django.shortcuts import render

# Create your views here.
#from django.contrib.auth.models import User
from rest_framework import viewsets
from rest.serializers import DeviceSerializer
from interface.models import Device


class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer