from enum import IntEnum
from dataclasses import dataclass


class DustyCastingType(IntEnum):
    SWING_WEAPON = 1
    THROW_WEAPON = 2


class DustyActiveAction(IntEnum):
    DEFAULT_SKILL_DOWN = 1
    DEFAULT_SKILL_UP = 2
    DEFAULT_SKILL_CANCEL = 3
    SPECIAL_SKILL_DOWN = 4
    SPECIAL_SKILL_UP = 5
    SPECIAL_SKILL_CANCEL = 6
    AIMING_LEFT = 7
    AIMING_RIGHT = 8
