from instructions.ADD import ADD
from instructions.BOMB import BOMB
from instructions.DIV import DIV
from instructions.JUMP import JUMP
from instructions.LOAD import LOAD
from instructions.LTJUMP import LTJUMP
from instructions.MOV import MOV
from instructions.MUL import MUL
from instructions.NEQJUMP import NEQJUMP
from instructions.NOP import NOP
from instructions.REVJUMP import REVJUMP
from instructions.REVLTJUMP import REVLTJUMP
from instructions.REVNEQJUMP import REVNEQJUMP
from instructions.SETIMMHIGH import SETIMMHIGH
from instructions.SETIMMLOW import SETIMMLOW
from instructions.STORE import STORE
from instructions.SUB import SUB
from instructions.TELEPORT import TELEPORT
from instructions.base import Instruction

INSTRUCTIONS: list[type[Instruction]] = [
    NOP,
    ADD,
    SUB,
    MUL,
    DIV,
    LOAD,
    STORE,
    MOV,
    JUMP,
    REVJUMP,
    LTJUMP,
    REVLTJUMP,
    NEQJUMP,
    REVNEQJUMP,
    SETIMMLOW,
    SETIMMHIGH,
    TELEPORT,
    BOMB
]