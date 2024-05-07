from enum import IntEnum
from dataclasses import dataclass


class ObjectState(IntEnum):
    IDLE = 1
    MOVING = 2
    HITTING = 3
    CASTING = 4
    DAMAGED = 5
    INVISIBLE = 6
    TARGETING = 7


@dataclass
class StateData:
    state: ObjectState  # how
    target: int = None  # whom
    value: any = None  # what
