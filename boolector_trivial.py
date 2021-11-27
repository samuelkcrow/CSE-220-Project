import pyboolector
from pyboolector import Boolector

# Create Bolector instance
b = Boolector()
# Enable model generation
b.Set_opt(pyboolector.BTOR_OPT_MODEL_GEN, True)
# Enable incrememntal solving (push/pop)
b.Set_opt(pyboolector.BTOR_OPT_INCREMENTAL, True)

# Create bit-vector sort of size 32
bvsort32 = b.BitVecSort(32)
# Create registers
r1 = b.Var(bvsort32, "r1")
r2 = b.Var(bvsort32, "r2")
r3 = b.Var(bvsort32, "r3")
# Create constants
r0 = b.Const(0, 32)

#----------------------Main Code-----------------------#

# Addi r1, r0, 4
r1 = r0 + 4
# Ld r3, 0(r1)
# Check load with addr in r1
b.Assert(r1 >= 0)
b.Assert(r1 < 8)
# Check smt
if b.Sat() == b.SAT:
    print("Load address: VALID")
else:
    print("Load address: INVALID")

# Add r1, r1, r1
r1 = r1 + r1
# Check load with addr in r1
b.Assert(r1 >= 0)
b.Assert(r1 < 8)
# Check smt
if b.Sat() == b.SAT:
    print("Load address: VALID")
else:
    print("Load address: INVALID")