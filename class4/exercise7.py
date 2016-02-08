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
    rtr2Dict = initRouter('cisco_ios', '50.76.53.27', 'pyclass', '88newclass', 8022)

    rtr2Conn = netmiko.ConnectHandler(**rtr2Dict)

    rtr2Conn.config_mode()
    if rtr2Conn.check_config_mode():
        rtr2Conn.send_command('logging buffered 512000')
        rtr2Conn.exit_config_mode()
    rtr2Conn.send_command('wr mem')
    print rtr2Conn.send_command('sh run | i logging')
