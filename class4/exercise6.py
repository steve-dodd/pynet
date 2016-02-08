#!/usr/bin/env python

import netmiko

def initRouter(devType, ipAddr, userName, passWord, port = 22, secret = ''):
    result = {'device_type' : devType,
            'ip' : ipAddr,
            'username' : userName,
            'password' : passWord,
            'port' : port,
            'secret' : secret}

    return result

if __name__ == "__main__":
    rtr1Dict = initRouter('cisco_ios', '50.76.53.27', 'pyclass', '88newclass')
    rtr1Conn = netmiko.ConnectHandler(**rtr1Dict)

    rtr2Dict = initRouter('cisco_ios', '50.76.53.27', 'pyclass', '88newclass', 8022)
    rtr2Conn = netmiko.ConnectHandler(**rtr2Dict)

    srxDict = initRouter('juniper', '50.76.53.27', 'pyclass', '88newclass', 9822)
    srxConn = netmiko.ConnectHandler(**srxDict)

    print rtr1Conn.send_command('show arp')
    print rtr2Conn.send_command('show arp')
    print srxConn.send_command('show arp')
