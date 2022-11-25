
import sys
import os.path
import sc
import importlib
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
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

inventory, converters, all_colors = sc.readSrcFile(filename)

vecs = { c:np.zeros(numRounds) for c in all_colors }

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
    for col,amt in inventory.items():
        vecs[col][r] = amt

colorplot = {col:col for col in all_colors}
colorplot['ship'] = 'red'
colorplot['barrel'] = 'orange'
colorplot['white'] = 'purple'

plt.clf()
for col,vec in vecs.items():
    if col != 'ship':
        plt.plot(range(numRounds), vec, color=colorplot[col], label=col)
plt.title(filename.replace(".src","").title())
plt.legend()
plt.ylim((0,numRounds*3))
pltsize = (6,3)
plt.savefig(filename.replace(".src",".png"), figsize=pltsize, dpi=600)

