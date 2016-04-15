#!/usr/bin/env python

from net_system.models import NetworkDevice
import django

def main():
    django.setup()

    devices = NetworkDevice.objects.all()

    for dev in devices:
        if 'test' in dev.device_name:
            dev.delete()

if __name__ == "__main__":
    main()
