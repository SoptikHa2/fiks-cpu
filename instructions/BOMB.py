from instructions.base import Instruction, ProgramError


class BOMB(Instruction):
    opcode = 0x50

    def execute(self) -> int:
        imm = self._parse_params(0, 16)
        _fill = self._parse_params(16, 8)

        if imm == 0:
            raise ProgramError("BOOM!")
        else:
            imm -= 1
            self._write_mem(self._pc, (self.opcode << 24) + (imm << 8) + _fill)

        return 1