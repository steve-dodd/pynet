#!/usr/bin/env python

import pexpect
from getpass import getpass

class router:
    def __init__(self, ipAddr = None, userName = None, port = 22):
        self.ipAddr = ipAddr
        self.userName = userName
        self.port = port
        self.passWord = '88newclass' #getpass()

        self.sshConn = pexpect.spawn('ssh -l {} {} -p {}'.format(self.userName,
                                                                 self.ipAddr,
                                                                 self.port))
        self.sshConn.timeout = 1
        self.sshConn.expect('[P|p]assword:')

        self.sendCmd(self.passWord)
        self.sendCmd('terminal length 0')

    def sendCmd(self, cmd):
        self.sshConn.sendline(cmd.rstrip())
        self.sshConn.expect('[#|>]')
        return self.sshConn.before

if __name__ == "__main__":
    rtr2 = router('50.76.53.27', 'pyclass', 8022)

    print rtr2.sendCmd('show ip interface brief')

