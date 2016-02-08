#!/usr/bin/env python

import traceback
import time

import paramiko
from getpass import getpass
import argparse

class router:
    def __init__(self, ip_addr = None, username = None, port = 22):
        self.BUFFER = 1024000
        self.ip_addr = ip_addr
        self.username = username
        self.password = "88newclass" #getpass()
        self.port = port

        self.remote_conn_pre = paramiko.SSHClient()
        self.remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.remote_conn_pre.connect(self.ip_addr, 
                                username = self.username, 
                                password = self.password, 
                                look_for_keys = False,
                                allow_agent = False, 
                                port = self.port)
        self.remote_conn = self.remote_conn_pre.invoke_shell()
        self.remote_conn.settimeout(1.0)
        self.send_cmd('terminal length 0')

    def send_cmd(self, cmd):
        self.remote_conn.send(cmd.rstrip() + '\n')
        while not self.remote_conn.recv_ready():
            time.sleep(100.0/1000.0)
        output = self.remote_conn.recv(self.BUFFER)
        return output

if __name__ == "__main__":
    x = router('50.76.53.27', 'pyclass', 8022)

    print x.send_cmd('sh ver')

