from net_system.models import NetworkDevice, Credentials

net_devices = NetworkDevice.objects.all()

for Device in net_devices:
    if 'sw' in Device.device_name:
        Device.vendor = 'arista'
    elif 'srx' in Device.device_name:
        Device.vendor = 'juniper'
    else:
        Device.vendor = 'cisco'
    Device.save()
    print Device, Device.vendor
