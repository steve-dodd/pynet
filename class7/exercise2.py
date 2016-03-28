#!/usr/bin/env python

import pyeapi
import argparse

def check_vlan(vlan):
    eapi_conn = pyeapi.connect_to("pynet-sw3")
    result = eapi_conn.enable("show vlan")
    vlan_list = result[0]['result']['vlans']

    if vlan in vlan_list:
        return True

    return False

def remove_vlan(vlan_id):
    eapi_conn = pyeapi.connect_to("pynet-sw3")
    eapi_conn.config("no vlan " + vlan_id)

def add_vlan(vlan_id, vlan_name):
    eapi_conn = pyeapi.connect_to("pynet-sw3")
    eapi_conn.config(["vlan " + vlan_id, "name " + vlan_name])

def main():
    parser = argparse.ArgumentParser(description='Item potent VLAN modifier')

    parser.add_argument('vlan_id', action="store")
    parser.add_argument('--remove', action="store_true", default=False, dest="remove_flag")
    parser.add_argument('--name', action="store", dest="vlan_name")

    args = parser.parse_args()

    vlan_id = args.vlan_id
    vlan_name =  args.vlan_name
    remove_flag = args.remove_flag

    if remove_flag == True:
        if check_vlan(vlan_id) == False:
            print vlan_id + " does not exist"
        else:
            remove_vlan(vlan_id)

    elif remove_flag == False:
        if check_vlan(vlan_id) == True:
            print vlan_id + " already exists"
        else:
            add_vlan(vlan_id, vlan_name)


if __name__ == "__main__":
    main()
