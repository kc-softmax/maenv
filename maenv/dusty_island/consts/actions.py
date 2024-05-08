from dataclasses import dataclass
from maenv.core.actions import ControlAction


@dataclass
class DustyControlAction(ControlAction):
    DEFAULT_SKILL_DOWN = 5
    DEFAULT_SKILL_UP = 6
    DEFAULT_SKILL_CANCEL = 7
    SPECIAL_SKILL_DOWN = 8
    SPECIAL_SKILL_UP = 9
    SPECIAL_SKILL_CANCEL = 10
