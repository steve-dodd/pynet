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

# Find IOS config lines with transform sets

obj_list = ios_cfg.find_objects(r"set transform-set")

# Determine crypto map membership

result = []
for o in obj_list:
    if not o.re_search(r"AES-SHA"):             #Find non-AES transforms
        result.append([o.parent.text, o.text])

for r in result:
    print r
