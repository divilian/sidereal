
import sys
import os.path
import glob
import sc
import importlib
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
importlib.reload(sc)

print("Sidereal Confluence simulator")

def runSim(filename, numRounds):
    inventory, converters, all_colors = sc.readSrcFile(filename)

    vecs = { c:np.zeros(numRounds) for c in all_colors }
    vecs['vpEquiv'] = np.zeros(numRounds)

    print("Initial inventory:")
    for i in inventory:
        print("  " + str(i))
    print("Initial converters:")
    for c in converters:
        print("  " + str(c))

    for r in range(numRounds):
        print("==============================")
        print(f"Round {r+1}:")
        sc.runRound(inventory, converters)
        print(f"\nInventory now:\n  {inventory}")
        for col,amt in inventory.items():
            vecs[col][r] = amt
        vecs['vpEquiv'][r] = sc.vpEquiv(inventory)

    colorplot = {col:col for col in all_colors}
    colorplot['ship'] = 'red'
    colorplot['barrel'] = 'orange'
    colorplot['white'] = 'purple'
    colorplot['vpEquiv'] = 'purple'

    plt.clf()
    for col,vec in vecs.items():
        if col != 'ship' and col != 'vpEquiv':
            plt.plot(range(numRounds), vec, color=colorplot[col], label=col)
        if col == 'vpEquiv':
            plt.plot(range(numRounds), vec, color="c", linewidth=2,
                linestyle="dashed", label=col)
    plt.title(filename.replace(".src","").title())
    plt.legend()
    plt.ylim((0,numRounds*3))
    pltsize = (6,3)
    plt.savefig(filename.replace(".src",".png"), dpi=600)


usage_msg = "Usage: sim.py startingCardsFile.src|ALL [numRounds]."

if len(sys.argv) not in [2,3]:
    sys.exit(usage_msg)

if len(sys.argv) == 3:
    numRounds = int(sys.argv[2])
else:
    numRounds = 6

if sys.argv[1] == 'ALL':
    for filename in glob.glob("*.src"):
        print(f"\n\nSimulating {filename.replace('.src','').title()}...")
        runSim(filename, numRounds)
elif not sys.argv[1].endswith(".src"): 
    sys.exit(usage_msg)
else:
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit(f"No such file {filename}.")
    runSim(filename, numRounds)


