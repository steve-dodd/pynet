#!/usr/bin/env python

import pynet_snmp

rtr1 = ("50.76.53.27", "galileo", 7961)
rtr2 = ("50.76.53.27", "galileo", 8061)
sysName = "1.3.6.1.2.1.1.5.0"
sysDescr = "1.3.6.1.2.1.1.1.0"

print pynet_snmp.snmp_get(rtr1, sysName)
print pynet_snmp.snmp_get(rtr2, sysName)
print pynet_snmp.snmp_get(rtr1, sysDescr)
print pynet_snmp.snmp_get(rtr2, sysDescr)
