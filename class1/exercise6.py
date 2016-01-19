import sys
import json
import yaml

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

# Generate list elements

dict = {}
for i in range (0, 10):
    dict[i] = i ** 2
list = []
for i in range (0, 10):
    list.append(i)
list.append(dict)
list.append("string")

# Create YAML file from list

with open(sys.argv[1], "w") as f:
    f.write(yaml.dump(list, default_flow_style=False))
f.close()

# Create JSON file from list

with open(sys.argv[2], "w") as f:
    json.dump(list, f)
f.close()

