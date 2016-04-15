#!/usr/bin/env python

from net_system.models import NetworkDevice
import django

def main():
    django.setup()

    test_dev1 = NetworkDevice(
        device_name='test-dev1',
        device_type='cisco_ios',
        ip_address='192.168.1.1',
        port=22,
    )
    test_dev1.save()

    test_dev2 = NetworkDevice.objects.get_or_create(
        device_name='test-dev2',
        device_type='cisco_ios',
        ip_address='192.168.1.2',
        port=8022,
    )
    print test_dev2

if __name__ == "__main__":
    main()
