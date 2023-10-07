from instructions.base import Instruction


class NOP(Instruction):
    opcode = 0x69

    def execute(self) -> int:
        return 1
