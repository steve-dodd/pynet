#!/usr/bin/env python

import pyeapi
import json
from pprint import pprint
pynet_sw3 = pyeapi.connect_to("pynet-sw3")

result = pynet_sw3.enable("show interfaces")

parse = result[0]['result']

interfaces = parse['interfaces']

for i in interfaces:
    print "Interface: " + i
    counters = interfaces[i]['interfaceCounters']
    print "inOctets: " + str(counters['inOctets'])
    print "outOctets: " + str(counters['outOctets'])

