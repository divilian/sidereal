
# Sidereal Confluence simulator classes/functions.

import re
import sys
from collections import defaultdict
import random

def readSrcFile(filename):
    with open(filename, encoding="utf-8") as f:
        if f.readline().rstrip() != "Inventory:":
            sys.exit(f"Illegal first line of {filename}.")
        converters = []
        inventory = Inventory()
        line = f.readline().rstrip()
        while line != "Converters:":
            inventory.addSpec(Spec.fromLine(line))
            line = f.readline().rstrip()
        line = f.readline().rstrip()
        while line:
            converters.append(Converter(line))
            line = f.readline().rstrip()
    return inventory, converters,\
        set.union(*[ c.all_colors() for c in converters ])


class Inventory(defaultdict):
    # https://stackoverflow.com/questions/45410638/how-can-i-inherit-defaultdict-and-use-its-copy-method-in-subclass-method
    def __init__(self,*args):
        if args:
            super(Inventory, self).__init__(*args)
        else:
            super(Inventory, self).__init__(int)

    def addSpec(self, spec):
        self[spec.color] += spec.amt

    # Add the contents of a second Inventory object to this one.
    def addInventory(self, inv2):
        for color, amt in inv2.items():
            self[color] += amt

    def consumeSpec(self, spec):
        self[spec.color] -= spec.amt

    def __repr__(self):
        if len(self) == 0:
            return "(empty inventory)"
        return ", ".join(
            [ f"{amt} {col if amt == 1 else col + 's'}"
                for col, amt in self.items() ] )

class Spec():
    @classmethod
    def fromLine(self, line):
        specPat = re.compile("(?P<col>[a-z]*):\s*(?P<amt>\d*)")
        matches = specPat.match(line)
        return Spec(matches['col'],matches['amt'])
        
    def __init__(self, color, amt):
        self.color = color
        self.amt = int(amt)

    def __repr__(self):
        return str(self.amt) + " " + \
            (self.color if self.amt == 1 else self.color + "s")


# Do inputs and outputs differ in anything important?
#class Requirement(Spec):
#    def __init__(self, color, amt):
#        super().__init__(color,amt)
#
#class Product(Spec):
#    def __init__(self, color, amt):
#        super().__init__(color,amt)


class Converter():

    def __init__(self):
        pass

    def __init__(self, line):
        self.reqs = set()
        self.prods = set()
        pat = re.compile(r"(?P<name>.*): \((?P<inp>.*)\) -> \((?P<outp>.*)\)")
        file_info = pat.match(line.strip())
        if not file_info:
            sys.exit(f"Malformed line: {line.strip()}.")
        self.name = file_info['name']
        self.reqs = self.process(file_info['inp'])
        self.prods = self.process(file_info['outp'])

    def process(self, line):
        if line == '':
            return set()
        pattern = re.compile(r"(?P<color>[a-z]+)(?P<amt>\d+)")
        parts = line.split(",")
        ret_val = set()
        for p in parts:
            line_info = pattern.match(p)
            ret_val |= {Spec(line_info['color'],line_info['amt'])}
        return ret_val

    def __repr__(self):
        rv = self.name.title() + ": "
        if self.reqs:
            rv += ' and '.join([ r.__repr__() for r in self.reqs ])
        else:
            rv += "(none)"
        rv += " -> "
        rv += ' and '.join([ r.__repr__() for r in self.prods ])
        return rv

    def canConvertWith(self, inputs):
        for req in self.reqs:
            if inputs[req.color] < req.amt:
                return False
        print(f"  Running {self.name}...")
        return True

    def all_colors(self):
        return { r.color for r in self.reqs } | \
            { p.color for p in self.prods }

    def convert(self, inputs, outputs):
        for req in self.reqs:
            inputs[req.color] -= req.amt
        for prod in self.prods:
            outputs[prod.color] += prod.amt


def runRound(inventory, converters):
    random.shuffle(converters)
    temp = Inventory()
    for c in converters:
        if c.canConvertWith(inventory):
            c.convert(inventory, temp)
    inventory.addInventory(temp)
