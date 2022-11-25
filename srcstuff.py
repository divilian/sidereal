
import re
import sys

class Spec():
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
        ret_val = self.name.title() + ": "
        ret_val += ' and '.join([ r.__repr__() for r in self.reqs ]) + " -> "
        ret_val += ' and '.join([ r.__repr__() for r in self.prods ])
        return ret_val

