from instructions.base import Instruction


class REVLTJUMP(Instruction):
    opcode = 0x13

    def execute(self) -> int:
        reg1 = self._parse_params(0, 4)
        reg2 = self._parse_params(4, 4)
        imm = self._parse_params(8, 16)

        if self._read_reg(reg1) < self._read_reg(reg2):
            return -imm

        return 1