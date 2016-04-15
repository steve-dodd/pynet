#!/usr/bin/env python

from net_system.models import NetworkDevice
import django
import netmiko
import time
import threading

def initRouter(devType, ipAddr, userName, passWord, port = 22, secret = ''):
    result = {'device_type' : devType,
            'ip' : ipAddr,
            'username' : userName,
            'password' : passWord,
            'port' : port,
            'secret' : secret}

    return result

def thread_send_cmd(dev_dict, cmd):
    dev_conn = netmiko.ConnectHandler(**dev_dict)
    print dev_conn.send_command(cmd)
    return

def main():
    startTime = time.time()

    django.setup()

    devices = NetworkDevice.objects.all()

    for itrDev in devices:
        devDict = initRouter(itrDev.device_type, itrDev.ip_address, itrDev.credentials.username, itrDev.credentials.password, itrDev.port)

        my_thread = threading.Thread(target=thread_send_cmd, args=(devDict, 'show version'))
        my_thread.start()

    main_thread = threading.currentThread()
    for itrThread in threading.enumerate():
        if itrThread is not main_thread:
            itrThread.join()

    finishTime = time.time()

    print "Threaded execution time was %s seconds" % str(finishTime - startTime)

if __name__ == "__main__":
    main()
