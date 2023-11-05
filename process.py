from dataclasses import dataclass

from instruction import execute_instruction
from instructions.base import ProgramError
from shared_state import SharedState

import config


@dataclass
class Process:
    state: SharedState
    pc: int
    registers: list[int]
    user_id: str
    executed_instructions: list[tuple[int, int]]
    alive: bool = True

    def __init__(self, state: SharedState, user_id: str):
        self.state = state
        self.pc = state.player_pc[user_id]
        self.registers = [0] * 8
        self.user_id = user_id
        self.executed_instructions = []

    def next(self):
        # if is not stuck at teleport rn
        if not self.user_id in self.state.player_teleport:
            self.executed_instructions.append((self.pc, self.state.memory[self.pc]))
        self.pc += execute_instruction(self.state, self.user_id, self.registers)
        self._normalize_pc()
        # If not in whitelist
        if len([x for x in config.PROGRAMS_ALLOWED_TO_REPEAT if self.user_id.endswith(x)]) == 0:
            # Check for repeats
            self.check_for_repetition(config.REPETITION_COUNT_LETHAL, config.MAX_SEQUENCE_LENGTH_CHECK)

    def kill(self):
        self.alive = False
        self.state.player_pc.pop(self.user_id)

    def check_for_repetition(self, num_of_repeats_needed: int, sequence_threshold: int):
        maximum_sequence_length = min(len(self.executed_instructions) // num_of_repeats_needed, sequence_threshold)
        for sequence_length in range(1, maximum_sequence_length):
            seq = self.executed_instructions[-sequence_length:]
            idx = len(self.executed_instructions) - sequence_length
            is_repeated = True
            for _ in range(num_of_repeats_needed):
                if self.executed_instructions[idx:sequence_length + idx] != seq:
                    is_repeated = False
                    break
                idx -= sequence_length
            if is_repeated:
                raise ProgramError(f"Sequence of instructions has been repeated {num_of_repeats_needed} times")

    def _normalize_pc(self):
        self.pc %= len(self.state.memory)
        self.state.player_pc[self.user_id] = self.pc

    def __repr__(self):
        return f"Process(pc={hex(self.pc)}, registers={[hex(x) for x in self.registers]}, user_id={self.user_id})"
