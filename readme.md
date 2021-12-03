# CSE 220 Project

A Boolector-enabled random RISC-V instruction sequence generator written in python

## Dependencies

```
pip3 install pyboolector
```

## Executing main program

* The main program is "boolector_riscv_smt.py"
* To change number of instructions change the constant "NUM_RAND_INSTRUCTIONS" in this file
* Register preconditions can be set in the "Initialize registers to 0" (add constants to r0 and boolector will automatically convert them to bitvectors)
* Memory precondition can be set in the "Write initial values to mem" section
```
python3 boolector_riscv_smt.py
```

## Executing other programs

* Binaries can be run in a risc-v 64-bit simulator but there's not much to them
* Z3 python files are abandoned and will not run without debugging (don't bother)
* Other boolector python files can be run in the same way as the main program, with slightly different functionality