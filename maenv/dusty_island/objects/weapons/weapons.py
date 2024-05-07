from __future__ import annotations
from maenv.core.actions import ControlAction
from maenv.core.objects.active_object import ActiveGameObject
from maenv.core.cardinal_direction import CardinalDirectionType


class Weapon(ActiveGameObject):
    """
        TODO description
    """

    damage = None
    attack_range = None
    targeting_range = 0
    targeting_angle = 0
    active_duration = None
    cooldown_duration = None

    def __init__(
        self,
        width: int,
        height: int,
        life: int,
    ) -> None:
        super(Weapon, self).__init__(
            [0, 0],
            width,
            height,
            life,
            0,
        )
        self.active_gauge = 0
        self.cooldown = 0

    def get_hit(self, damage: int) -> bool:
        hitting = super().get_hit(damage)
        if self.life < 1:
            self.active_gauge = 0
        return hitting

    def require_auto_targeting(self) -> bool:
        return False

    def is_activated(self) -> bool:
        return self.active_gauge > 0

    def activate(self, direction_type: CardinalDirectionType = None) -> Weapon | None:
        if direction_type:
            self.update_direction(direction_type)
        if self.cooldown > 0:
            return None
        if self.active_gauge < 1:
            self.active_gauge = self.active_duration
            self.cooldown = self.cooldown_duration
            self.life = 1
            return self
        return None

    def sync(self, target: tuple[int, int]):
        super().sync(target)
        if self.cooldown > 0:
            self.cooldown -= 1

    def act(self):
        super().act()
        if self.active_gauge > 0:
            self.active_gauge -= 1
        else:
            self.life = 0


class ThrowWeapon(Weapon):

    max_power_gauge = 10

    def __init__(
        self,
        width: int,
        height: int,
        life: int,
        min_speed: int,
    ) -> None:
        super(ThrowWeapon, self).__init__(
            width,
            height,
            life,
        )
        self.min_speed = min_speed
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

    def require_auto_targeting(self) -> bool:
        return self.preparing

    def prepare(self):
        self.force_direction_vector = None
        self.preparing = True
        self.power_gauge = 1

    def activate(self, direction_type: CardinalDirectionType = None) -> Weapon | None:
        if weapon := super().activate(direction_type):
            self.preparing = False
            return weapon
        return None

    def sync(self, target: tuple[int, int]):
        # 던지는 무기는 가지고 있을때만 sync를 맞춘다.
        if not self.is_activated():
            super().sync(target)
        if self.preparing:
            self.power_gauge += 1

    def act(self):
        self.actions.append(ControlAction.FORWARD)
        self.speed = self.min_speed + self.power_gauge
        self.power_gauge -= 1
        super().act()
