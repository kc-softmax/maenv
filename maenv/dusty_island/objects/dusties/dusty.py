import pygame
from maenv.core.actions import ControlAction
from maenv.core.state import ObjectState
from maenv.core.objects.active_object import ActiveGameObject
from maenv.dusty_island.consts.dusty import (
    DUSTY_SIZE,
    DUSTY_LIFE,
    DUSTY_SPEED,
    DUSTY_PROTECTION_TIME
)
from maenv.dusty_island.consts.actions import DustyActiveAction
from maenv.dusty_island.objects.weapons import Weapon


class Dusty(ActiveGameObject):

    vision_range = 10
    damage_protection_time = DUSTY_PROTECTION_TIME

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
        self.pending_weapons: list[Weapon] = []
        self.aiming_vector = pygame.Vector2(0, 1)
        self.weapon: Weapon = None

    def pickup_weapon(self, weapon: Weapon):
        weapon.owner_id = self.short_id
        weapon.follow_direction(self.direction)
        self.update_state(ObjectState.PICKUP, value=str(weapon))
        self.weapon = weapon

    def release_weapon(self):
        # 던지거나... 기타 등등?
        self.update_state(ObjectState.DROP, value=str(self.weapon))
        self.weapon = None

    def cancel_movement(self):
        super().cancel_movement()
        self.weapon and self.weapon.sync(self.center)

    def handle_actions(self, action: int):
        if not self.weapon:
            return
        action = DustyActiveAction(action)
        match action:
            case DustyActiveAction.DEFAULT_SKILL_DOWN:
                if weapon := self.weapon.activate(action):
                    self.pending_weapons.append(weapon)
            case DustyActiveAction.SPECIAL_SKILL_DOWN:
                if self.weapon.prepare():
                    self.aiming_vector = self.direction.get_vector().copy()
            case DustyActiveAction.SPECIAL_SKILL_UP:
                if weapon := self.weapon.activate(action):
                    weapon.force_direction_vector = self.aiming_vector
                    self.pending_weapons.append(weapon)
            case DustyActiveAction.AIMING_LEFT:
                self.aiming_vector.rotate_ip(-5)
            case DustyActiveAction.AIMING_RIGHT:
                self.aiming_vector.rotate_ip(5)

    def render(self, surface: pygame.Surface):
        if self.damage_protection > 0:
            if self.damage_protection % 2 != 0:
                pygame.draw.rect(surface, self.render_color, self)
        else:
            pygame.draw.rect(surface, self.render_color, self)
        self.weapon and self.weapon.render(surface)

    def act(self):
        super().act()
        self.weapon and not self.weapon.throwing and self.weapon.sync(
            self.center)

    def update_object(self):
        super().update_object()
        # activate 상태이면 env에서 update 한다.
        self.weapon and not self.weapon.is_activated() and self.weapon.update_object()
