from dataclasses import dataclass, field

from process import Process

@dataclass
class TurnSnapshot:
    registers: list[int]
    next_instruction: int
    memory: list[int]
    memory_dump_start: int | None
    pc: int | None = None


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

    def init_players(self, players: list[str]):
        for player in players:
            self.players[player] = PlayerLog([])

    def append_turn(self, process: Process):
        player_id = process.user_id
        registers = process.registers.copy()
        instruction = process.state.memory[process.pc]

        memory = []
        memory_dump_start = None
        if self.log_memory:
            memory = process.state.memory.copy()
            memory_dump_start = 0

        self.players[player_id].turns.append(TurnSnapshot(registers, instruction, memory, memory_dump_start, process.pc))

    def record_death(self, process: Process, reason: str):
        player_id = process.user_id
        self.players[player_id].death_reason = reason
        self.survived[player_id] = len(self.players[player_id].turns)

    def set_winner(self, process: Process):
        self.winner = process.user_id
        self.survived[process.user_id] = len(self.players[process.user_id].turns)

    def cut_log(self, max_turns: int):
        for player in self.players.keys():
            self.players[player].turns = self.players[player].turns[:max_turns]
