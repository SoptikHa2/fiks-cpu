from instructions.base import Instruction

_SPENT_CYCLES_WAITING: dict[str, int] = {}


class TELEPORT(Instruction):
    opcode = 0x42

    def execute(self) -> int:
        timeout = self._parse_params(0, 8)
        jmp = self._parse_params(8, 16)

        # If there is someone to teleport with
        if len([x for x in self._state.player_teleport if x != self._player_id]) > 0:
            to_teleport = self._state.player_teleport.pop()

            self._state.player_pc[to_teleport] = self._pc + 1
            # Return value so that we are moved to the other player's PC
            return (self._state.player_pc[to_teleport] + 1) - self._pc
        else:
            self._state.player_teleport.add(self._player_id)

            if self._player_id in _SPENT_CYCLES_WAITING:
                _SPENT_CYCLES_WAITING[self._player_id] += 1
                if _SPENT_CYCLES_WAITING[self._player_id] > timeout:
                    _SPENT_CYCLES_WAITING[self._player_id] = 0
                    self._state.player_teleport.remove(self._player_id)
                    return jmp
            else:
                _SPENT_CYCLES_WAITING[self._player_id] = 0

        return 0
