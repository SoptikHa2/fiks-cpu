from instructions.base import Instruction, ProgramError


class DIV(Instruction):
    opcode = 0x04

    def execute(self) -> int:
        reg1 = self._parse_params(0, 4)
        reg2 = self._parse_params(4, 4)
        imm = self._parse_params(8, 16)

        if self._read_reg(reg2) + imm == 0:
            raise ProgramError("Division by zero")

        self._write_reg(reg1, self._read_reg(reg1) // (self._read_reg(reg2) + imm))

        return 1