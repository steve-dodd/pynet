#!/usr/bin/env python

import snmp_helper
import sys

def snmp_get(device, oid):
    snmp_data = snmp_helper.snmp_get_oid(device, oid = oid)
    return snmp_helper.snmp_extract(snmp_data)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit("Usage: exercise.py COMMUNITY IP_ADDR OID PORT")
    else:
        community = sys.argv[1]
        ip_addr = sys.argv[2]
        oid = sys.argv[3]
        port = sys.argv[4]
        device = (ip_addr, community, port)

        print snmp_get(device, oid)
