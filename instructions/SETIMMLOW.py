from instructions.base import Instruction, ProgramError


class SETIMMLOW(Instruction):
    opcode = 0x20

    def execute(self) -> int:
        reg1 = self._parse_params(0, 4)
        imm = self._parse_params(8, 16)

        old_value = self._read_reg(reg1) & 0xFFFF0000
        self._write_reg(reg1, imm | old_value)

        return 1