# Here be dragons

This is an interpreter of a made-up assembly-like language for [FIKS](https://fiks.fit.cvut.cz/): [task](https://fiks.fit.cvut.cz/files/tasks/season10/round2/bitva.pdf). This is not production-ready code, it was hacked together in few days. This is not how I usually write code, I promise.

## How to run

If you don't know how to setup python environemnt: install python3, poetry. Run `poetry shell` and `poetry install` afterwards. You need to do the `poetry shell` in every terminal in which you want to run the program.

To run, use `python3 main.py LOG_LEVEL PATH/TO/SOURCE/1 PATH/TO/SOURCE/2 ...`

`LOG_LEVEL`: `0` to log nothing, `1` to log everything, `2` to log only memory near current PC. Returns json log of the execution.

Source code is in the format described below. See [factorial](factorial.fiks) implementation.

## Overview of the language

This might be slightly out of date/impreicse and serves just as a quick overview, see the [task description](https://fiks.fit.cvut.cz/files/tasks/season10/round2/bitva.pdf) and the source code.

- Supports up to 4 programs at once
- There is total of `N*256` instructions of memory available, which is the total amount of memory of a program
- Data and code are stored in the same memory
- Reading from memory cell `42` returns closest program's PC
- Reading from memory cell `43` returns second-closest program's PC
- One can overwrite its own code
- The goal is to survive
- One can die by:
  - Executing invalid instruction
  - Executing bomb with timer remaining = 0
  - Looping three times without changing the underlying instructions
- One can kill other programs by finding out their location and overwriting their code
- Each program has 6 (8 for real) 32-bit registers. Register 0 always contains a zero.
- All registers are zero-ed out in the beginning.
- Trying to overwrite register `0` kills the program, as it is invalid operation.
- All numbers are unsigned 32-bit integers
- Each instruction is 4 bytes wide
  - NOP: `0x69 ?? ?? ??` (in place of `??`, all bytes are valid)
  - ADD/SUB/MUL (div is secret `0x4`): `0x01/02/03(8b) reg1(4b) reg2(4b) imm(16b)`. ie, `reg1 += reg2 + imm`.
  - LOAD: `0x05  reg1(4b) reg2(4b) imm(16b)`. `reg1 = mem[reg2 + imm]`
  - STORE: `0x06 reg1(4b) reg2(4b) imm(16b)`. `mem[reg2 + imm] = reg1`
  - MOV: `0x07 reg1(4b) reg2(4b) imm(16b)`. `reg1 = reg2 + imm`
  - JUMP: `0x10 reg1(4b) reg2(4b) imm(16b)`. `if (reg1 == reg2) pc += imm`
  - REVJUMP: `0x11 reg1(4b) reg2(4b) imm(16b)`. `if (reg1 == reg2) pc -= imm`
  - LTJUMP: `0x12 ...`, if `reg1 < reg2` then `pc += imm`
  - REVLTJUMP: `0x13 ...`, if `reg1 < reg2` then `pc -= imm`
  - NEQJUMP: `0x14 ...`, if `reg1 != reg2` then `pc += imm`
  - REVNEQJUMP: `0x15 ...`, if `reg1 != reg2` then `pc -= imm`
  - SETIMMLOW: `0x20 reg1(4b) ??(4b) imm(16b)`. `reg1[low] = imm`
  - SETIMMHIGH: `0x21 reg1(4b) ??(4b) imm(16b)`. `reg1[high] = imm`
  - TELEPORT: `0x42 IMM1(8b) IMM2(16b)`: freezes program until another one calls teleport. Timeout: IMM1 cycles.
    If times out, jumps to PC+IMM2.
    When another program calls teleport, those two programs swap their PC and continue.
  - BOMB: `0x50 imm(16b) ?? ??`. Decrements its `imm` by 1 each time it is executed.
    If it is zero before decrementing, the bomb fires, destroying the process that executed it.

You can write instructions via hex codes.

For example, the following code will loop.

```
69 00 00 00  ; NOP
11 00 00 01  ; REVJUMP reg0, reg0, 0x0001
```

Secret: the following code places bomb in front of closest enemy process.

```
; Get other program's PC
05 10 00 2b ; LOAD reg1 = mem[reg0 + 43] ; ENEMY PC ; 0
01 10 00 04 ; ENEMY PC += 4 ; 1
; Prepare bomb
21 20 50 00 ; reg2 = BOMB 0? ?? ?? ; 2
; Place it there
06 21 00 00 ; mem[ENEMY PC + 1] = BOMB 0 ; 3
; Jump back and start again
11 00 00 03 ; REVJUMP reg0, reg0, 0x0004
```
