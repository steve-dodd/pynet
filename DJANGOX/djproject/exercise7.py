#!/usr/bin/env python

from net_system.models import NetworkDevice
import django
import netmiko
import time
import multiprocessing

def initRouter(devType, ipAddr, userName, passWord, port = 22, secret = ''):
    result = {'device_type' : devType,
            'ip' : ipAddr,
            'username' : userName,
            'password' : passWord,
            'port' : port,
            'secret' : secret}

    return result

def multiproc_show_ver(dev_dict):
    dev_conn = netmiko.ConnectHandler(**dev_dict)
    return dev_conn.send_command('show version')

def main():
    startTime = time.time()

    django.setup()

    devices = NetworkDevice.objects.all()

    devList = []

    for itrDev in devices:
        devDict = initRouter(itrDev.device_type,
                            itrDev.ip_address,
                            itrDev.credentials.username,
                            itrDev.credentials.password,
                            itrDev.port)
        devList.append(devDict)

    procPool = multiprocessing.Pool(8)
    print(procPool.map(multiproc_show_ver, devList))

    finishTime = time.time()

    print "Multiproc execution time was %s seconds" % str(finishTime - startTime)

if __name__ == "__main__":
    main()
