from dataclasses import dataclass, field

from process import Process


@dataclass
class TurnSnapshot:
    registers: list[int]
    next_instruction: int
    memory: list[int]
    memory_dump_start: int | None


@dataclass
class PlayerLog:
    turns: list[TurnSnapshot]
    death_reason: str | None = None


@dataclass
class Log:
    log_memory: bool
    players: dict[str, PlayerLog] = field(default_factory=dict)
    winner: str | None = None
    survived: dict[str, int] = field(default_factory=dict)

    def append_turn(self, process: Process):
        player_id = process.user_id
        registers = process.registers.copy()
        instruction = process.state.memory[process.pc]

        memory = []
        memory_dump_start = None
        if self.log_memory:
            memory = process.state.memory[max(0, process.pc - 10):min(len(process.state.memory) - 1, process.pc + 10)]
            memory_dump_start = max(0, process.pc - 10)

        if player_id not in self.players:
            self.players[player_id] = PlayerLog([])
        self.players[player_id].turns.append(TurnSnapshot(registers, instruction, memory, memory_dump_start))

    def record_death(self, process: Process, reason: str):
        player_id = process.user_id
        if player_id not in self.players:
            self.players[player_id] = PlayerLog([])
        self.players[player_id].death_reason = reason
        self.survived[player_id] = len(self.players[player_id].turns)

    def set_winner(self, process: Process):
        self.winner = process.user_id
        self.survived[process.user_id] = len(self.players[process.user_id].turns)
