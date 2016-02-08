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

    rtrConnList = [rtr1Conn, rtr2Conn]

    for itr_rtrConn in rtrConnList:
        itr_rtrConn.config_mode()
        if itr_rtrConn.check_config_mode():
            itr_rtrConn.send_config_from_file('logging_changes.conf')
            itr_rtrConn.exit_config_mode()
        itr_rtrConn.send_command('wr mem')
        print itr_rtrConn.send_command('sh run | i logging')
