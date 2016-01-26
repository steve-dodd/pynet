#!/usr/bin/env python

import telnetlib
import time
import socket
import sys
import getpass

class Router_Connection:
    def __init__(self, ip_addr, username, password, port = 23, timeout = 6, remote_conn = None):
        self.ip_addr = ip_addr
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password
        self.remote_conn = remote_conn
        try:
            self.remote_conn = telnetlib.Telnet(ip_addr, port, timeout)
            self.remote_conn.read_until("[Uu]sername:", timeout)
            self.remote_conn.write(username + '\n')
            self.remote_conn.read_until("[Pp]assword:", timeout)
            self.remote_conn.write(password + '\n')
            self.remote_conn.read_until("[#>]", timeout)
            self.remote_conn.write("term len 0\n")
        except socket.timeout:
            print "Connection timed-out: " + ip_addr

    def Send_Cmd(self, cmd):
        if self.remote_conn == None:
            return "Connection not established: " + self.ip_addr
        else:
            cmd = cmd.rstrip()
            self.remote_conn.write(cmd + '\n')
            time.sleep(1)
            return self.remote_conn.read_very_eager()

if __name__ == "__main__":
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    rc = Router_Connection(ip_addr, username, password, 23, 1)
    
    print rc.Send_Cmd('sh ip int bri')
