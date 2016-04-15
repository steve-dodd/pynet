from net_system.models import NetworkDevice, Credentials

net_devices = NetworkDevice.objects.all()
creds = Credentials.objects.all()

for Device in net_devices:
    if 'sw' in Device.device_name:
        Device.credentials = creds[1]
    else:
        Device.credentials = creds[0]
    Device.save()
