#!/usr/bin/env python
import sys
import socket
import snmp_helper
from getpass import getpass
import json

def snmp_v3_get(router, snmp_user, oid):
    snmp_data = snmp_helper.snmp_get_oid_v3(router, snmp_user, oid)
    snmp_text = snmp_helper.snmp_extract(snmp_data)
    return snmp_text

def compare(prev_state, curr_state):
    if curr_state[2] != prev_state[2] and curr_state[2] != 0:
        return False
    else:
        return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit("Usage: script.py IP_ADDR PORT")

    ip_addr = sys.argv[1]
    port = sys.argv[2]
    username = raw_input("Username: ")
    auth_key = getpass("Authentication Key: ")
    encrypt_key = getpass("Encryption Key: ")
    router = (ip_addr, port)
    snmp_user = (username, auth_key, encrypt_key)

    oid_list = [
    ('sysUptime', '1.3.6.1.2.1.1.3.0'),
    ('ccmHistoryRunningLastChanged', '1.3.6.1.4.1.9.9.43.1.1.1.0'),
    ('ccmHistoryRunningLastSaved', '1.3.6.1.4.1.9.9.43.1.1.2.0'), 
    ('ccmHistoryStartupLastChanged', '1.3.6.1.4.1.9.9.43.1.1.3.0')]

    curr_state = []

    for oid in oid_list:
        result = snmp_v3_get(router, snmp_user, oid[1])
        curr_state.append( (oid[0], oid[1], result) )

    print curr_state

    '''try:
        f = open("prev_state.json", "w")
        prev_state = json.load(f)
        print compare(prev_state, curr_state)
        json.dump(curr_state, f)
    except NameError:
        json.dump(curr_state, f)
    '''
