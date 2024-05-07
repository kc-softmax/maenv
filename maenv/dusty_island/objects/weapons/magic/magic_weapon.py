from __future__ import annotations

from pygame import Vector2
from maenv.core.objects.game_object import GameObject
from maenv.dusty_island.objects.artifact import Artifact
from maenv.dusty_island.objects.weapons import Weapon
from maenv.dusty_island.consts.weapons.magic_weapons import (
    MAGIC_WEAPON_SIZE,
    MAGIC_WEAPON_ACTIVE_DURATION
)


class MagicWeapon(Weapon):

    active_duration = MAGIC_WEAPON_ACTIVE_DURATION
    equippable_artifacts_type = []

    def __init__(
        self,
    ) -> None:
        super(MagicWeapon, self).__init__(
            MAGIC_WEAPON_SIZE,
            MAGIC_WEAPON_SIZE,
            1)
        self.artifact: Artifact = None
        self.weapon_direction: Vector2 = None
        self.cooldown = 0

    def activate_artifact(self) -> list[GameObject]:
        raise NotImplementedError()

    def set_artifact(self, artifact: Artifact):
        if artifact.artifact_type not in self.equippable_artifacts_type:
            raise Exception('')
        self.artifact = artifact

    def cast_spell(self) -> list[GameObject] | None:
        return self.activate_artifact()
