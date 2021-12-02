#!/usr/bin/env python3
# Script to generate random RISC-V instruction sequences
# and use the z3 SMT solver to prove they don't seg-fault

from z3 import *
import random

def check_asm_add_sub_load(add_val, sub_val, addr_imm_val, \
        min_addr_val, max_addr_val):
    # Z3 declerations
    s=Solver()
    add,sub,addr=Ints('add sub addr')
    # Creating boolean assertions in Z3
    s.add(addr==addr_imm_val+add_val-sub_val)
    s.add(add==add_val)
    s.add(sub==sub_val)
    s.add(addr>min_addr_val)
    s.add(addr<max_addr_val)
    #Checking SATisfiability
    result = s.check()
    print(s.assertions())
    return result == sat

print(check_asm_add_sub_load(10, 3, 15, 0, 40))

class Inst:
    def __init__(self, op, rd, rs1, rs2, imm):
        self.op = op
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = imm

    def print(self):
        print(self.op, self.rd, self.rs1, self.rs2, self.imm)
    
    op_list = ['add', 'addi', 'sub', 'subi', 'ld']
    imm_min = -2048
    imm_max = 2047

def rand_inst(num_regs):
    inst = Inst(random.choice(Inst.op_list), \
        random.randrange(num_regs), \
        random.randrange(num_regs), \
        random.randrange(num_regs), \
        random.randrange(Inst.imm_min, Inst.imm_max))
    return inst


def rand_inst_seq(num_inst, num_regs):
    inst_sequence = []
    for i in range(num_inst):
        inst_sequence.append(rand_inst(num_regs))
    return inst_sequence

def solve_inst_seq(inst_seq, num_regs):
    a = AstRef()
    regs = []
    for i in range(num_regs):
        regs.append(0)
    for inst in inst_seq:
        if inst.op == 'add':
            s.add(regs[inst.rd - 1]==regs[inst.rs1 -1]+regs[inst.rs2 - 1])
    print(s.check())
    print(s.assertions())


if __name__ == '__main__':
    min_addr = 0
    max_addr = 10000

    inst_seq = rand_inst_seq(5, 3)
    for inst in inst_seq:
        inst.print()
    solve_inst_seq(inst_seq, 3)