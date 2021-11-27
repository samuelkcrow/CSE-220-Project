#!/usr/bin/env python3
# Just trying to figure out z3 don't mind me

from z3 import *
import random

s = Solver()

CPU = Datatype('CPU')
CPU.declare('cons', \
    ('pc', IntSort()), \
    ('r0', IntSort()), \
    ('r1', IntSort()), \
    ('r2', IntSort()), \
    ('segfault', BoolSort()))
CPU = CPU.create()

def mk_cpu_state(pc, r0, r1, r2, sf):
    return CPU.cons(pc, r0, r1, r2, sf)

def mk_cpu_add_transition(cpu):
    pc = simplify(CPU.pc(cpu))
    r0 = simplify(CPU.r0(cpu))
    r1 = simplify(CPU.r1(cpu))
    r2 = simplify(CPU.r2(cpu))
    cpu = mk_cpu_state(pc + 1, r0, r1, r2 + r1, False)
    s.push()
    s.append(False)
    return cpu

def mk_cpu_load_transition(cpu):
    pc = simplify(CPU.pc(cpu))
    r0 = simplify(CPU.r0(cpu))
    r1 = simplify(CPU.r1(cpu))
    r2 = simplify(CPU.r2(cpu))
    if r2 > 10:
        sf = True
    else:
        sf = False
    cpu = mk_cpu_state(pc + 1, r0, r1, r2, sf)
    s.push()
    s.append(sf)
    return cpu

def validate_cpu_state():
    if s.check() == sat:
        return True
    else:
        s.pop()
        return False

cpu = mk_cpu_state(0, 0, 1, 2, False)
# print(simplify(CPU.r2(cpu)))
for _ in range(11):
    cpu_new = mk_cpu_add_transition(cpu)
    print(simplify(cpu_new))
    if validate_cpu_state():
        cpu = cpu_new
    cpu_new = mk_cpu_load_transition(cpu)
    print(simplify(cpu_new))
    if validate_cpu_state():
        cpu = cpu_new

# condition = []
# condition.append(add(1, 2))
# condition.append(add(2, 2))

# s = Solver()
# s.add(*condition)

# print(s.check())
# # print(s.model())