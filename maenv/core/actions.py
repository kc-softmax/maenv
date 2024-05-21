from typing import Optional
from dataclasses import dataclass
from enum import IntEnum
from maenv.core.direction import DirectionType


class ActionType(IntEnum):
    WHEEL_CONTROL = 1
    IMMEDIATE_CONTROL = 2
    ACTIVE = 3


class WheelAction(IntEnum):
    FORWARD = 1
    ROTATE_LEFT = 2
    ROTATE_RIGHT = 3
    STOP = 4


@dataclass
class ControlAction:
    """
        각 env 마다 다른 action들을 가지고 있을것이다.
        상속받아 사용한다.
    """
    action_type: ActionType
    action_value: Optional[int] = None

    def __post_init__(self):
        # 유효성 검사를 진행해야 한다.
        pass

    # stop = 1
    # # for wheel mode
    # forward = 2
    # rotate_left = 3
    # rotate_right = 4
    # # for immediate mode
    # move = 5
    # move_direction: DirectionType = None

    # # 유효성 검사해야한다.
    # def __init
