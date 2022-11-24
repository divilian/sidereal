
import sys
import os.path
import srcstuff
import importlib
importlib.reload(srcstuff)

print("Sidereal Confluence simulator")

usage_msg = "Usage: sim.py startingCardsFile.src."

if len(sys.argv) != 2:
    sys.exit(usage_msg)
if not sys.argv[1].endswith(".src"): 
    sys.exit(usage_msg)
filename = sys.argv[1]

if not os.path.exists(filename):
    sys.exit(f"No such file {filename}.")

with open(filename, encoding="utf-8") as f:
    converters = [ srcstuff.Converter(l) for l in f.readlines() ]

for c in converters:
    print(c)
