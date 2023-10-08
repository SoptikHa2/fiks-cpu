from dataclasses import dataclass, field

from process import Process


@dataclass
class TurnSnapshot:
    registers: list[int]
    memory: list[int]
    next_instruction: int

@dataclass
class PlayerLog:
    turns: list[TurnSnapshot]
    death_reason: str | None = None

@dataclass
class Log:
    players: dict[str, PlayerLog] = field(default_factory=dict)
    winner: str | None = None
    survived: dict[str, int] = field(default_factory=dict)

    def append_turn(self, process: Process):
        player_id = process.user_id
        registers = process.registers
        memory = process.state.memory[max(0,process.pc-10):min(len(process.state.memory)-1, process.pc+10)]
        instruction = process.state.memory[process.pc]

        if player_id not in self.players:
            self.players[player_id] = PlayerLog([])
        self.players[player_id].turns.append(TurnSnapshot(registers, memory, instruction))

    def record_death(self, process: Process, reason: str):
        player_id = process.user_id
        self.players[player_id].death_reason = reason
        self.survived[player_id] = len(self.players[player_id].turns)

    def set_winner(self, process: Process):
        self.winner = process.user_id
        self.survived[process.user_id] = len(self.players[process.user_id].turns)
