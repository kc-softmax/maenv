from enum import IntEnum
from dataclasses import dataclass


class ObjectState(IntEnum):
    IDLE = 1  # 뭔가 state를 남겨야하는데, 마땅한게 없을때, (멈추거나)
    MOVING = 2  # 움직일때
    HITTING = 3  # 도끼가 적중했다. (axe의 state)
    CASTING = 4  # 도끼 휘두르기, 돌 던지기 (dusty의 state)
    DAMAGED = 5  # damege를 받았을때
    TARGETING = 6  # 내가 누군가를 타겟으로 잡았을때
    TARGETED = 7  # 내가 누군가의 타겟이 되었을대


@dataclass
class StateData:
    state: ObjectState  # how
    target: int = None  # whom
    value: any = None  # what
