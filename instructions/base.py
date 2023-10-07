from abc import ABC, abstractmethod

from shared_state import SharedState


class ProgramError(Exception):
    pass


class Instruction(ABC):
    opcode: int

    def __init__(self, state: SharedState, player_id: str, params: int, registers: list[int]):
        self._state = state
        self._player_id = player_id
        self._pc = state.player_pc[player_id]
        self._params = params
        self._registers = registers
        self._memory = state.memory

    @abstractmethod
    def execute(self) -> int:
        """
        Execute an instruction, modifying registers, memory and returning target PC.
        If the program should terminate, an exception will be thrown.
        """
        ...

    def _parse_params(self, skip_bits: int, take_bits: int) -> int:
        mask = 0xFFFFFF >> skip_bits
        bits_to_skip_at_the_end = 24 - (take_bits + skip_bits)
        return (self._params & mask) >> bits_to_skip_at_the_end

    def _read_reg(self, reg: int) -> int:
        if reg == 0:
            return 0

        if reg < 0 or reg >= len(self._registers):
            raise ProgramError(f"Invalid register {reg}")
        return self._registers[reg]

    def _write_reg(self, reg: int, value: int):
        if reg < 0 or reg >= len(self._registers):
            raise ProgramError(f"Invalid register {reg}")
        self._registers[reg] = value % 0xFFFFFFFF

    def _read_mem(self, address: int) -> int:
        if address == 42:
            return self._pc
        elif address == 43:
            if len(self._state.player_pc) == 1:
                return self._pc

            player_pcs = list(self._state.player_pc.values())
            player_distances = [
                (
                    min((pc - self._pc) % len(self._memory),
                        (self._pc - pc) % len(self._memory)),
                    pc
                )
                for pc in player_pcs if pc != self._pc]
            player_distances.sort(key=lambda x: x[0])
            return player_distances[0][1]

        if address < 0 or address >= len(self._memory):
            raise ProgramError(f"Invalid memory address {address}")
        return self._memory[address]

    def _write_mem(self, address: int, value: int):
        if address < 0 or address >= len(self._memory):
            raise ProgramError(f"Invalid memory address {address}")
        self._memory[address] = value % 0xFFFFFFFF
