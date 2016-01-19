import sys
import json
import yaml
import pprint

# File error handling

try:
    if sys.argv[1]:
        pass
except IndexError:
    print "Specify a YAML file"
    exit(-1)

try:
    if sys.argv[2]:
        pass
except IndexError:
    print "Specify a JSON file"
    exit(-1)

# Open YAML file and pprint

with open(sys.argv[1]) as f:
    yaml_list = yaml.load(f)
f.close()

print "YAML file: " + sys.argv[1]
pprint.pprint(yaml_list)

# Open JSON file and pprint

with open(sys.argv[2]) as f:
    json_list = json.load(f)
f.close()

print "JSON file: " + sys.argv[2]
pprint.pprint(json_list)
