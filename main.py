import orjson as json
import sys
from pathlib import Path
from typing import Tuple

from instructions.base import ProgramError
from log import Log
from process import Process
from shared_state import SharedState


def load_program_instructions(path: Path) -> list[int]:
    with open(path, "r") as f:
        for line in f:
            if ';' in line:
                line = line[:line.index(';')]
            line = line.replace(" ", "").replace("\t", "").strip()

            if len(line) == 0:
                continue
            if len(line) != 8:
                raise ValueError(f"Invalid instruction: {line}")

            yield int(line, 16)


def create_program(sources: list[Tuple[str, list[int]]]) -> list[Process]:
    mem = [0] * (len(sources) + 1) * 256

    # Generate programs
    starting_pc = 256
    starting_pcs = {}
    processes = []
    state = SharedState(mem, starting_pcs)

    for source in sources:
        if len(source[1]) > 256:
            raise ValueError("Program too long. Must be at most 256 bytes")

        instr = starting_pc
        starting_pcs[source[0]] = starting_pc
        processes.append(Process(state, source[0]))
        for instruction in source[1]:
            mem[instr] = instruction
            instr += 1

        starting_pc += 256

    return processes


def main():
    sources: list[Tuple[str, list[int]]] = []
    log_memory = sys.argv[1]
    log: Log = Log(log_memory=log_memory == "1")

    # Get source code
    for file in sys.argv[2:]:
        sources.append((file, list(load_program_instructions(Path(file)))))

    if len(sources) == 0 or len(sources) > 8:
        raise ValueError("Invalid number of programs. Must be between 1 and 8")

    processes = create_program(sources)

    log.init_players([p.user_id for p in processes])

    limit_iters = 0
    while sum([p.alive for p in processes]) > 1:
        limit_iters += 1
        if limit_iters > 10000:
            for p in processes:
                if p.alive:
                    p.kill()
                    log.record_death(p, "Timed out")
            break

        for p in processes:
            if p.alive:
                try:
                    p.next()
                    log.append_turn(p)
                except ProgramError as e:
                    p.kill()
                    log.record_death(p, str(e))

    if len(alive := [p for p in processes if p.alive]) == 1: # We have a winner!
        log.set_winner(alive[0])

    print(json.dumps(log).decode("utf-8"))


if __name__ == '__main__':
    main()
