from dataclasses import dataclass, field


@dataclass
class SharedState:
    memory: list[int]
    player_pc: dict[str, int]
    player_teleport: set[str] = field(default_factory=set)