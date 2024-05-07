from __future__ import annotations

from enum import IntEnum

MAX_AGENTS = 64
MAX_ARTIFACT_COUNT_AT_ONCE = 10
MAX_AQUIRE_ARTIFACTS = 4
# via max_agents
ARTIFACT_RATIO = 0
TREE_RATIO = 0.1


class Team(IntEnum):
    COLONISTS = 1
    GUARDIANS = 2
