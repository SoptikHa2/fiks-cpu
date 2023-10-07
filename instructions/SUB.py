from instructions.base import Instruction


class SUB(Instruction):
    opcode = 0x02

    def execute(self) -> int:
        reg1 = self._parse_params(0, 4)
        reg2 = self._parse_params(4, 4)
        imm = self._parse_params(8, 16)

        self._write_reg(reg1, self._read_reg(reg1) - (self._read_reg(reg2) + imm))

        return 1