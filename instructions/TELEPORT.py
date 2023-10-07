from instructions.base import Instruction, ProgramError


class TELEPORT(Instruction):
    opcode = 0x42

    def execute(self) -> int:
        timeout = self._parse_params(0, 8)
        jmp = self._parse_params(8, 16)

        raise ValueError("Not implemented yet")