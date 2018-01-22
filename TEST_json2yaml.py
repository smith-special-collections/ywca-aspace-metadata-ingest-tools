from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import json

print("Enter/Paste your JSON. Ctrl-D to save it.")
contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)

data = json.loads("\n".join(contents))

print(dump(data, Dumper=Dumper, default_flow_style=False))
