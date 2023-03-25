import parsy as p
import numpy as np


class Polynom:
    def __init__(self, order):
        self.d = np.zeros(10)
        self.d[order] = 1.0

    def smul(self, k):
        self.d *= k
        return self

    def add(self, other):
        if other is None:
            return self
        self.d += other.d
        return self

    def eval(self, x):
        y = 0.0
        for i,k in enumerate(self.d):
            y += k * x**i
        return y

    def __repr__(self):
        return "+".join(f"{self.d[i]}x^{i}"for i in reversed(range(len(self.d))) if self.d[i]!=0)

ids = {}

def add_to_ids(name, poly):
    ids[name] = poly

number = p.regex("[0-9]+").map(int)
var = p.string("x")

pow = ((var << p.string("^")) >> number).map(Polynom)
times = p.seq(number << p.string("*").optional(), pow).combine(lambda k,polynom: polynom.smul(k))
stimes = (number << p.string("*").optional() << var).map(lambda x: Polynom(1).smul(x))

item =  pow | times | stimes | number.map(lambda x: Polynom(0).smul(x)) | var.map(lambda _: Polynom(1))

add = p.forward_declaration()
add.become(p.seq(item, (p.string("+") >> add).optional()).combine(lambda left, right: left.add(right)))

idfun = p.regex("[a-z]+")

defpoly = p.seq(idfun << p.regex(r"\s*:\s*"), add).combine(add_to_ids)
eval = p.seq(idfun << p.string("("), number << p.string(")")).combine(lambda id, value: print(ids[id].eval(value)))

statement = defpoly | eval | idfun.map(lambda id: print(ids[id]))

program = p.forward_declaration()
program.become(p.seq(statement, (p.string(";") >> program).optional()))

program.parse("f: 1+x^5+x^3;f;f(0);f(5);g:x+1;g;g(10)")

