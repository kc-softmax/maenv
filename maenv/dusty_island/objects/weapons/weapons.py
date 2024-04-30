from __future__ import annotations
from maenv.core.objects.active_object import ActiveGameObject
from maenv.core.cardinal_direction import CardinalDirectionType


class Weapon(ActiveGameObject):

    damage = None
    attack_range = None
    active_duration = None
    cooldown_duration = None

    def __init__(
        self,
        width: int,
        height: int,
        life: int,
        speed: int,
    ) -> None:
        super(Weapon, self).__init__(
            [0, 0],
            width,
            height,
            life,
            speed,
        )
        self.active_count = 0
        self.cooldown = 0

    def deactivate(self):
        self.active_count = 0

    def is_activate(self) -> bool:
        return self.active_count > 0

    def activate(self, direction_type: CardinalDirectionType = None) -> Weapon | None:
        if direction_type:
            self.update_direction(direction_type)
        if self.cooldown > 0:
            return None
        if self.active_count < 1:
            self.active_count = self.active_duration
            self.cooldown = self.cooldown_duration
            return self
        return None

    def sync(self, target: tuple[int, int]):
        super().sync(target)
        if self.cooldown > 0:
            self.cooldown -= 1

    def act(self) -> bool:
        if self.active_count > 0:
            self.active_count -= 1
        return True


class ThrowWeapon(Weapon):

    def sync(self, target: tuple[int, int]):
        if self.active_count < 1:
            super().sync(target)
        else:
            # sync를 호출하지 않지만, 쿨타임은 줄어들어야 한다, 이문제는 해결해야 함
            if self.cooldown > 0:
                self.cooldown -= 1
