import sys
from pathlib import Path
from typing import Tuple

from instructions.base import ProgramError
from process import Process
from shared_state import SharedState


def load_program_instructions(path: Path) -> list[int]:
    with open(path, "r") as f:
        for line in f:
            if ';' in line:
                line = line[:line.index(';')]
            line = line.replace(" ", "").replace("\t", "")

            if len(line) == 0:
                continue
            if len(line) != 8:
                raise ValueError(f"Invalid instruction: {line}")

            yield int(line, 16)


def main():
    sources: list[Tuple[str, list[int]]] = []

    # Get source code
    for file in sys.argv[1:]:
        sources.append((file, list(load_program_instructions(Path(file)))))

    if len(sources) == 0 or len(sources) > 8:
        raise ValueError("Invalid number of programs. Must be between 1 and 8")

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

    limit_iters = 0
    while sum([p.alive for p in processes]) > 1:
        limit_iters += 1
        if limit_iters > 10000:
            break

        for p in processes:
            if p.alive:
                try:
                    p.next()
                    print(p)
                except ProgramError as e:
                    print(f"Program {p.user_id} terminated with error: {e}")
                    p.kill()


if __name__ == '__main__':
    main()
