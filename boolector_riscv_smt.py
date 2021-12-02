import random
import pyboolector
from pyboolector import Boolector#, BoolectorException

#---------------------Arguments------------------------#
NUM_RAND_INSTRUCTIONS = 100000

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
    print("add a%d, a%d, a%d" % (rd, rs1, rs2))
    return regs_get(rs1) + regs_get(rs2)

def Addi(rd, rs1, rs2, imm):
    print("addi a%d, a%d, %i" % (rd, rs1, imm))
    return regs_get(rs1) + imm

def Lw(rd, rs1, rs2, imm):
    print("lw a%d, 0(a%d)" % (rd, rs1), end=" ")
    rs1 = regs_get(rs1)
    b.Push()
    b.Assert(rs1 >= r0)
    b.Assert(rs1 < 8)
    if b.Sat() == b.SAT:
        print("")
        b.Pop()
        return mem[rs1[2:]]
    else:
        print("//ADDRESS INVALID, DELETE THIS INSTRUCTION")
        b.Pop()
        return -1

###### I decided to comment out Sw instruction because
###### it's complicated to follow its execution in a sequence
# def Sw(rd, rs1, rs2, imm):
#     print("sw a%d, 0(a%d)" % (rs1, rs2))
#     rs1 = regs_get(rs1)
#     rs2 = regs_get(rs2)
#     b.Push()
#     b.Assert(rs1 >= r0)
#     b.Assert(rs1 < 8)
#     if b.Sat() == b.SAT:
#         print("Store address: VALID")
#         global mem
#         mem = b.Write(mem, rs1[2:], rs2)
#         b.Pop()
#         return 0
#     else:
#         print("Store address: INVALID")
#         b.Pop()
#         return -1

# Define operations list
ops_list = [Add, Addi, Lw]

def Rand_Inst():
    rd  = random.randint(1, 3)
    rs1 = random.randint(0, 3)
    rs2 = random.randint(0, 3)
    imm = random.randrange(8)
    op  = random.choice(ops_list)
    result = op(rd, rs1, rs2, imm)
    if result >= 0: # Filter out invalid loads
        regs_set(rd, r0 + result)
    return

#----------------------Main Code-----------------------#

# Initialize registers to 0
r1 = r0 + r0
r2 = r0 + r0
r3 = r0 + r0

# Write initial values to mem
mem = b.Write(mem, 0, 0x00)
mem = b.Write(mem, 1, 0x11)
mem = b.Write(mem, 2, 0x22)
mem = b.Write(mem, 3, 0x33)
mem = b.Write(mem, 4, 0x44)
mem = b.Write(mem, 5, 0x55)
mem = b.Write(mem, 6, 0x66)
mem = b.Write(mem, 7, 0x77)

b.Sat()
print("Contents of a1, a2, a3")
regs_list = [r1, r2, r3]
for reg in regs_list:
    print(reg.assignment)

print("\nRandom instruction sequence of length", NUM_RAND_INSTRUCTIONS)

for _ in range(NUM_RAND_INSTRUCTIONS):
    Rand_Inst()

b.Sat()
print("\nContents of a1, a2, a3")
regs_list = [r1, r2, r3]
for reg in regs_list:
    print(reg.assignment)
