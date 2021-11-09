#!/usr/bin/env python3

from z3 import *
import random

def check_asm_add_sub_load(add_val, sub_val, addr_imm_val, min_addr_val, max_addr_val):
    s=Solver()
    add,sub,addr=Ints('add sub addr')
    s.add(addr==addr_imm_val+add_val-sub_val)
    s.add(add==add_val)
    s.add(sub==sub_val)
    s.add(addr>min_addr_val)
    s.add(addr<max_addr_val)
    result = s.check()
    #print(result)
    #print (s.model())
    return result == sat

# print(check_asm_add_sub_load(0,0,10000,0,20000))
# print(check_asm_add_sub_load(0,0,10000,0,1000))

class RiscvInst:
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

def random_riscv_inst(num_regs):
    inst = RiscvInst(random.choice(RiscvInst.op_list), \
        random.randrange(num_regs), \
        random.randrange(num_regs), \
        random.randrange(num_regs), \
        random.randrange(RiscvInst.imm_min, RiscvInst.imm_max))
    return inst


def random_riscv_sequence(num_instructions, num_regs):
    inst_sequence = []
    for i in range(num_instructions):
        inst_sequence.append(random_riscv_inst(num_regs))
    return inst_sequence


min_addr = 0
max_addr = 10000

inst_seq = random_riscv_sequence(5, 3)
for inst in inst_seq:
    inst.print() 