
import sys
import os.path
import sc
import importlib
importlib.reload(sc)

print("Sidereal Confluence simulator")

usage_msg = "Usage: sim.py startingCardsFile.src [numRounds]."

if len(sys.argv) not in [2,3]:
    sys.exit(usage_msg)
if not sys.argv[1].endswith(".src"): 
    sys.exit(usage_msg)
filename = sys.argv[1]
if len(sys.argv) == 3:
    numRounds = int(sys.argv[2])
else:
    numRounds = 5

if not os.path.exists(filename):
    sys.exit(f"No such file {filename}.")

inventory, converters = sc.readSrcFile(filename)

print("Initial inventory:")
for i in inventory:
    print("  " + str(i))
print("Initial converters:")
for c in converters:
    print("  " + str(c))

for r in range(numRounds):
    print("==============================")
    print(f"Round {r}:")
    sc.runRound(inventory, converters)
    print(f"\nInventory now:\n  {inventory}")


