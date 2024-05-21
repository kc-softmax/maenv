from __future__ import annotations
from enum import IntEnum

ITEM_PICKUP_DURATION = 30
MAX_AGENTS = 64
# via max_agents
TREE_RATIO = 0.1


class WeaponType(IntEnum):
    NORMAL_AXE = 1
