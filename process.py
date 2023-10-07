from dataclasses import dataclass

from instruction import execute_instruction
from shared_state import SharedState


@dataclass
class Process:
    state: SharedState
    pc: int
    registers: list[int]
    user_id: str
    memory_size: int
    alive: bool = True

    def __init__(self, state: SharedState, user_id: str):
        self.state = state
        self.pc = state.player_pc[user_id]
        self.registers = [0] * 8
        self.user_id = user_id

    def next(self):
        self.pc += execute_instruction(self.state, self.user_id, self.registers)
        self._normalize_pc()

    def kill(self):
        self.alive = False
        self.state.player_pc.pop(self.user_id)

    def _normalize_pc(self):
        self.pc %= len(self.state.memory)
        self.state.player_pc[self.user_id] = self.pc

    def __repr__(self):
        return f"Process(pc={hex(self.pc)}, registers={[hex(x) for x in self.registers]}, user_id={self.user_id})"
