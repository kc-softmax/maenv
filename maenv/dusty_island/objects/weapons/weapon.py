from __future__ import annotations
import math
import pygame
import maenv.utils.colors as colors
from warnings import warn
from maenv.core.actions import ControlAction, ActionType, WheelAction
from maenv.core.objects.active_object import ActiveGameObject
from maenv.dusty_island.consts.actions import DustyActiveAction


class Weapon(ActiveGameObject):

    is_wheel_direction = True
    render_color = colors.CRIMSON

    swing_attack_range = None
    swing_active_duration = None
    throw_active_duration = None
    cooldown_duration = None

    swing_angle = 1
    max_power_gauge = 1
    power_accelation = 0.5
    min_throw_speed = 1
    throw_limit = -1
    active_life = 1
    knockback_power = 0

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        super(Weapon, self).__init__(
            [0, 0],
            width,
            height,
            0,
            0,
        )
        self.active_gauge = 0
        self.cooldown = 0
        self.throwing = False
        self.preparing = False
        self._power_gauge = 0

    @property
    def power_gauge(self):
        return self._power_gauge

    @power_gauge.setter
    def power_gauge(self, value: int):
        if value > self.max_power_gauge:
            self._power_gauge = self.max_power_gauge
        elif value < 0:
            self._power_gauge = 0
        else:
            self._power_gauge = value

    def is_activated(self) -> bool:
        return self.active_gauge > 0

    def deactivated(self):
        self.life = 0
        self.active_gauge = 0

    def get_damage(self) -> int:
        warn('weapon class should be override this method')

    def get_hit(self, damage: int) -> bool:
        hitting = super().get_hit(damage)
        if self.life < 1:
            self.active_gauge = 0
        return hitting

    def prepare(self) -> bool:
        if self.preparing:
            return False
        if self.cooldown > 0 or self.is_activated():
            return False
        self.preparing = True
        self.power_gauge = 1
        return True

    def activate(
        self,
        action: DustyActiveAction,
    ) -> Weapon | None:
        if self.cooldown > 0:
            return None
        if self.is_activated():
            return None

        self.throwing = action == DustyActiveAction.SPECIAL_SKILL_UP
        if self.throwing:
            if not self.preparing:
                return None
            self.active_gauge = self.throw_active_duration
            self.cooldown = self.cooldown_duration + self.power_gauge
            if self.throw_limit > 0:
                self.throw_limit -= 1
        else:
            self.active_gauge = self.swing_active_duration
            self.cooldown = self.cooldown_duration
        self.life = self.active_life
        self.preparing = False
        return self

    def update_object(self):
        super().update_object()
        if self.preparing:
            self.power_gauge += 1
        if self.cooldown > 0:
            self.cooldown -= 1
        self.is_activated() and not self.life and self.deactivated()

    def swing_act(self):
        progress = self.active_gauge / self.swing_active_duration
        axe_direction = self.direction.get_vector().rotate(
            self.swing_angle / 2 - self.swing_angle * progress
        ).normalize()
        # 원의 방정식을 사용하여 x, y 좌표 계산
        offset_x = self.width * 0.5 + self.swing_attack_range
        offset_y = self.height * 0.5 + self.swing_attack_range
        self.centerx = math.floor(self.centerx + offset_x * axe_direction.x)
        self.centery = math.floor(self.centery + offset_y * axe_direction.y)

    def throw_act(self):
        self.actions.append((
            ControlAction(ActionType.WHEEL_CONTROL, WheelAction.FORWARD)))
        self.speed = self.min_throw_speed + self.power_gauge * self.power_accelation
        self.power_gauge -= 1

    def act(self):
        # 오로지 activate 일때만 호출된다.
        if not self.is_activated():
            self.deactivated()
            return
        if self.throwing:
            self.throw_act()
        else:
            self.swing_act()
        self.active_gauge -= 1
        super().act()
