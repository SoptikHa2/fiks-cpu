from instructions import INSTRUCTIONS
from instructions.base import ProgramError
from shared_state import SharedState


def execute_instruction(state: SharedState, player_id: str, registers: list[int]) -> int:
    """
    Execute an instruction, modifying registers, memory and returning target PC.
    If the program should terminate, an exception will be thrown.
    """
    pc = state.player_pc[player_id]
    command = state.memory[pc]

    opcode = (command & 0xFF000000) >> 0x18

    target_instruction = [instr for instr in INSTRUCTIONS if instr.opcode == opcode]

    if len(target_instruction) != 1:
        raise ProgramError(f"Unknown opcode {opcode}")

    return target_instruction[0](state, player_id, command & 0x00FFFFFF, registers).execute()
