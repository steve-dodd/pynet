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

# Find IOS config lines with pfs group2

obj_list = ios_cfg.find_objects(r"set pfs group2")


# Determine crypto map membership

result = []
for o in obj_list:
    result.append(o.parent.text)

for r in result:
    print r
