#!/usr/bin/env python

import netmiko
import multiprocessing
import time

def initRouter(devType, ipAddr, userName, passWord, port = 22, secret = ''):
    result = {'device_type' : devType,
            'ip' : ipAddr,
            'username' : userName,
            'password' : passWord,
            'port' : port,
            'secret' : secret}

    return result

def multiProcShowArpDevDict(devDict):
    devConn = netmiko.ConnectHandler(**devDict)
    return devConn.send_command('show arp')

if __name__ == "__main__":
    startTime = time.time()

    rtr1Dict = initRouter('cisco_ios', '50.76.53.27', 'pyclass', '88newclass')
    rtr2Dict = initRouter('cisco_ios', '50.76.53.27', 'pyclass', '88newclass', 8022)
    srxDict = initRouter('juniper', '50.76.53.27', 'pyclass', '88newclass', 9822)

    procPool = multiprocessing.Pool(8)
    print(procPool.map(multiProcShowArpDevDict, [rtr1Dict, rtr2Dict, srxDict]))

    finishTime = time.time()

    print "Multiprocess execution took %s seconds" % str(finishTime - startTime)

