#!/usr/bin/env python

import telnetlib
import sys
import time
import socket

class Router_Connection:
    def __init__(self, ip_addr, port = 23, timeout = 1, username = None, password = None):
        self.ip_addr = ip_addr
        self.port = port
        self.timeout = timeout
        self.username = username
        self.password = password

def Open_Connection(Router_Connection):
    try:
        remote_conn = telnetlib.Telnet(Router_Connection.ip_addr, Router_Connection.port, Router_Connection.timeout)
        remote_conn.read_until("[Uu]sername:", Router_Connection.timeout)
        remote_conn.write(Router_Connection.username + "\n")
        remote_conn.read_until("[Pp]assword:", Router_Connection.timeout)
        remote_conn.write(Router_Connection.password + "\n")
        remote_conn.read_until("[#>]", Router_Connection.timeout)
        remote_conn.write("terminal length 0\n")
        return remote_conn
    except socket.timeout: 
        sys.exit("Connection timeout: " + Router_Connection.ip_addr)

def Send_Command(remote_conn, command):
    command = command.rstrip()
    remote_conn.write(command + "\n")
    remote_conn.flush()
    time.sleep(1)
    return remote_conn.read_very_eager()

if __name__ == "__main__":
    import getpass

    if len(sys.argv) < 2:
        print "Usage: excercise2.py IP_ADDRESS [PORT] [TIMEOUT]"
    else:
        ip_addr = sys.argv[1]
        port = 23
        timeout = 1
        try:
            if sys.argv[2]:
                port = sys.argv[2]
        except IndexError:
            pass
        try:
            if sys.argv[3]:
                timeout = sys.argv[3]
        except IndexError:
           pass
        username = raw_input("Username: ")
        password = getpass.getpass("Password: ")
        r = Router_Connection(ip_addr, port, timeout, username, password)
        r_conn = Open_Connection(r)

        print Send_Command(r_conn, "show ip int bri")
 
        r_conn.close()
