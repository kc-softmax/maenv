from __future__ import annotations
import numpy as np
from enum import IntEnum

ARTIFACT_SIZE = 16
DEFAULT_ARTIFACT_WEIGHT = 10
SPECIAL_ARTIFACT_WEIGHT = 0.5

SHOTGUN_BULLET_COUNT = 3

BUSTER_CALL_BOMB_COUNT = 15
BUSTER_CALL_BOMB_RADIUS = 256
BUSTER_CALL_SPAWN_DELAY = 30


class ArtifactType(IntEnum):
    WOLF = 1
    BEAR = 2
    TIGER = 3
    SHOTGUN = 10
    POISON_BOMB = 11
    BUSTER_CALL = 12

    @classmethod
    def get_random_type(
        cls,
        np_random: np.random.Generator,
        size=1
    ) -> ArtifactType | list[ArtifactType]:
        # Define the artifacts and their corresponding weights
        artifacts = list(cls)
        special_artifact = [cls.TIGER, cls.BUSTER_CALL]

        weights = []
        for artifact in artifacts:
            if artifact in special_artifact:
                weights.append(SPECIAL_ARTIFACT_WEIGHT)
            else:
                weights.append(DEFAULT_ARTIFACT_WEIGHT)

        # The choice method selects items based on their weights
        return np_random.choice(
            artifacts, size=size, p=np.array(weights) / sum(weights))
