import pygame
import collections
from maenv.core.actions import ControlAction
from maenv.core.objects.game_object import GameObject
from maenv.core.objects.active_object import ActiveGameObject

from maenv.dusty_island.consts.game import (
    Team,
    MAX_AQUIRE_ARTIFACTS
)
from maenv.dusty_island.consts.artifact import (
    ArtifactType
)
from maenv.dusty_island.consts.dusty import (
    DUSTY_SIZE,
    DUSTY_LIFE,
    DUSTY_SPEED
)
from maenv.dusty_island.objects.weapons import Weapon, ThrowWeapon
from maenv.dusty_island.objects.weapons.magic import MagicWeapon
from maenv.dusty_island.objects.artifact import Artifact


class Dusty(ActiveGameObject):

    vision_range = 10

    def __init__(
        self,
        agent_name: str,
    ) -> None:
        super(Dusty, self).__init__(
            [0, 0],
            DUSTY_SIZE,
            DUSTY_SIZE,
            DUSTY_LIFE,
            DUSTY_SPEED)
        self.agent_name = agent_name
        self.artifacts: list[Artifact] = []
        self.pending_weapons: list[Weapon | MagicWeapon] = []

        self.team: Team = None
        self.normal_weapon: Weapon = None
        self.magic_weapon: MagicWeapon = None

    def cancel_movement(self):
        super().cancel_movement()
        self.normal_weapon and self.normal_weapon.sync(
            self.center)
        self.magic_weapon and self.magic_weapon.sync(
            self.center)

    def get_artifact(self, artifact_type: ArtifactType) -> Artifact:
        return next((
            artifact
            for artifact in self.artifacts
            if artifact.artifact_type == artifact_type), None)

    def acquire_item(self, item: GameObject) -> bool:
        if isinstance(item, Artifact):
            if not self.magic_weapon:
                return False
            if item.artifact_type not in self.magic_weapon.equippable_artifacts_type:
                return False
            if len(self.artifacts) < MAX_AQUIRE_ARTIFACTS:
                self.artifacts.append(item)
                return True
        return False

    def remove_item(self, item: GameObject) -> bool:
        if isinstance(item, Artifact):
            self.artifacts.remove(item)
        return True

    def handle_actions(self, action: ControlAction):
        # ACTIVE_SKILL_1 기본 공격에 대해서만 처리한다.
        match action:
            case ControlAction.ACTIVE_SKILL_1:
                # normal weapon 이 사용가능한 상태인지 확인
                if weapon := self.normal_weapon.activate(self.direction.current_direction):
                    self.pending_weapons.append(weapon)
                    return
            case ControlAction.ACTIVE_SKILL_2:
                if not self.magic_weapon.artifact:
                    return
                if magic_weapon := self.magic_weapon.activate(self.direction.current_direction):
                    if magics := magic_weapon.cast_spell():
                        self.pending_weapons.extend(magics)
                        self.magic_weapon.artifact = self.get_artifact(
                            self.magic_weapon.artifact.artifact_type)
                        self.remove_item(self.magic_weapon.artifact)
                        return

    def render(self, surface: pygame.Surface):
        super().render(surface)
        self.normal_weapon and self.normal_weapon.render(surface)
        self.magic_weapon and self.magic_weapon.render(surface)

    def act(self) -> bool:
        super().act()
        self.normal_weapon and self.normal_weapon.sync(self.center)
        self.magic_weapon and self.magic_weapon.sync(self.center)
        return self.life > 0
