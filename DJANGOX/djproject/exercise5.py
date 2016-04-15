#!/usr/bin/env python

from net_system.models import NetworkDevice
import django
import netmiko
import time

def initRouter(devType, ipAddr, userName, passWord, port = 22, secret = ''):
    result = {'device_type' : devType,
            'ip' : ipAddr,
            'username' : userName,
            'password' : passWord,
            'port' : port,
            'secret' : secret}

    return result

def main():
    startTime = time.time()

    django.setup()

    devices = NetworkDevice.objects.all()

    for itrDev in devices:
        devDict = initRouter(itrDev.device_type, itrDev.ip_address, itrDev.credentials.username, itrDev.credentials.password, itrDev.port)
        devConn = netmiko.ConnectHandler(**devDict)

        print devConn.send_command('show version')

        finishTime = time.time()

    print "Serial execution time was %s seconds" % str(finishTime - startTime)

if __name__ == "__main__":
    main()
