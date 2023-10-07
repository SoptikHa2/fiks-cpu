from instructions.base import Instruction, ProgramError


class STORE(Instruction):
    opcode = 0x6

    def execute(self) -> int:
        reg1 = self._parse_params(0, 4)
        reg2 = self._parse_params(4, 4)
        imm = self._parse_params(8, 16)

        self._write_mem(self._read_reg(reg2) + imm, self._read_reg(reg1))

        return 1