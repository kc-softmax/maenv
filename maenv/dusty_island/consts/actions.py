from enum import IntEnum
from dataclasses import dataclass
from maenv.core.actions import ControlAction


class DustyCastingType(IntEnum):
    VERTICAL_AXE_SWING = 1
    THROW_STONE = 2


@dataclass
class DustyControlAction(ControlAction):
    DEFAULT_SKILL_DOWN = 5
    DEFAULT_SKILL_UP = 6
    DEFAULT_SKILL_CANCEL = 7
    SPECIAL_SKILL_DOWN = 8
    SPECIAL_SKILL_UP = 9
    SPECIAL_SKILL_CANCEL = 10
