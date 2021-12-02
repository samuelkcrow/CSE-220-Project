import random
import pyboolector
from pyboolector import Boolector#, BoolectorException

#---------------------SMT Setup------------------------#

# Create Bolector instance
b = Boolector()
# Enable model generation
b.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, True)
# Enable incrememntal solving (push/pop)
b.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, True)

#----------------Initialize Variables------------------#

# Create bit-vector sorts of size 3 and 32
bvsort3 = b.BitVecSort(3)
bvsort32 = b.BitVecSort(32)
# Create memory array sort of size 3addrbits x 32bits
arrsort = b.ArraySort(bvsort3, bvsort32)
# Create memory
mem = b.Array(arrsort, "mem_arr")
# Create registers
r1 = b.Var(bvsort32, "r1")
r2 = b.Var(bvsort32, "r2")
r3 = b.Var(bvsort32, "r3")
# Create constants
r0 = b.Const(0, 32)




#----------------Function Declerations-----------------#

def regs_get(regid):
    regs = [r0, r1, r2, r3]
    return regs[regid]

def regs_set(regid, val):
    if regid == 1:
        global r1
        r1 = val
    elif regid == 2:
        global r2
        r2 = val
    else:
        global r3
        r3 = val

def Add(rd, rs1, rs2, imm):
    print("add r%d, r%d, r%d" % (rd, rs1, rs2))
    return regs_get(rs1) + regs_get(rs2)

def Addi(rd, rs1, rs2, imm):
    print("addi r%d, r%d, %i" % (rd, rs1, imm))
    return regs_get(rs1) + imm

def Lw(rd, rs1, rs2, imm):
    print("lw r%d, 0(r%d)" % (rd, rs1))
    b.Push()
    b.Assert(regs_get(rs1) >= r0)
    b.Assert(regs_get(rs1) < 1)
    if b.Sat() == b.SAT:
        print("Load address: VALID")
        b.Pop()
        return 8
    else:
        print("Load address: INVALID")
        b.Pop()
        return -1

# Define operations collection
ops_list = [Add, Addi, Lw]

def Rand_Inst():
    rd  = random.randint(1, 3)
    rs1 = random.randint(0, 3)
    rs2 = random.randint(0, 3)
    imm = random.randrange(8)
    op  = random.choice(ops_list)
    result = op(rd, rs1, rs2, imm)
    if result >= 0:
        regs_set(rd, r0 + result)
    else:
        print("Omit pervious instruction")
    return


#----------------------Main Code-----------------------#

r1 = r0 + r0
r2 = r0 + r0
r3 = r0 + r0

# # Add r1, r0, r0
# r1 = Add(1, 0, 0, 0)
# # Add r2, r0, r0
# r2 = Add(2, 0, 0, 0)
# # Add r3, r0, r0
# r3 = Addi(3, 0, 0, 100)

regs_list = [r0, r1, r2, r3]
b.Sat()
for reg in regs_list:
    print(reg.assignment)

Rand_Inst()
Rand_Inst()
Rand_Inst()
Rand_Inst()
Rand_Inst()
Rand_Inst()

regs_list = [r0, r1, r2, r3]
b.Sat()
for reg in regs_list:
    print(reg.assignment)

# # Write 0 values to mem
# mem = b.Write(mem, 0, 0)
# mem = b.Write(mem, 1, 0)
# mem = b.Write(mem, 2, 0)
# mem = b.Write(mem, 3, 0)
# mem = b.Write(mem, 4, 0)
# mem = b.Write(mem, 5, 0)
# mem = b.Write(mem, 6, 0)
# mem = b.Write(mem, 7, 0)