#!/usr/bin/env python3
# Just trying to figure out z3 don't mind me

from z3 import *
import random

# a = Int('a')
# print(a.sort())
# b = Int('b')
# print((a + b).params)

CPU = Datatype('CPU')
CPU.declare('cons', \
    ('pc', IntSort()), \
    ('r0', IntSort()), \
    ('r1', IntSort()), \
    ('r2', IntSort()))
CPU = CPU.create()
cpu = CPU.cons(0, 0, 1, 2)

print(cpu)


# def init_condition():
#     return And(True)

# def add(a_in, b_in):
#     a = Int('a')
#     b = Int('b')
#     return And(a_in == b_in)

# condition = []
# condition.append(add(1, 2))
# condition.append(add(2, 2))

# s = Solver()
# s.add(*condition)

# print(s.check())
# # print(s.model())