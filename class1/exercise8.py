import ciscoconfparse
import sys

# File error handling

try:
    if sys.argv[1]:
        pass
except IndexError:
    print "Specify a Cisco IOS configuration file"
    exit(-1)

ios_cfg = ciscoconfparse.CiscoConfParse(sys.argv[1])

crypto_list = ios_cfg.find_objects(r"^crypto map CRYPTO")

for l in crypto_list:
    print l.text
    for child in l.children:
        print child.text
