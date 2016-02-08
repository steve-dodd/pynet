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
        self.sshConn.timeout = 3
        self.sshConn.expect('[P|p]assword:')

        self.sendCmd(self.passWord)
        self.sendCmd('terminal length 0')

    def sendCmd(self, cmd):
        self.sshConn.sendline(cmd.rstrip())
        self.sshConn.expect('[#|>]')
        return self.sshConn.before

if __name__ == "__main__":
    rtr2 = router('50.76.53.27', 'pyclass', 8022)

    rtr2.sendCmd('conf t')
    rtr2.sendCmd('logging buffered 64000')
    rtr2.sendCmd('end')
    rtr2.sendCmd('wr mem')
    print rtr2.sendCmd('show run')
