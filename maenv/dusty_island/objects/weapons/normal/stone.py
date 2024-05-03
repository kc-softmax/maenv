import math
from maenv.core.actions import ControlAction
from maenv.core.cardinal_direction import CardinalDirectionType
from maenv.dusty_island.objects.weapons import ThrowWeapon
from maenv.dusty_island.consts.weapons.normal_weapons import (
    NORMAL_STONE_DAMAGE,
    NORMAL_STONE_ATTACK_RANGE,
    NORMAL_STONE_COOLDOWN,
    NORMAL_STONE_LIFE,
    NORMAL_STONE_SIZE,
    NORMAL_STONE_SPEED,
)
from maenv.dusty_island.objects.weapons.weapons import Weapon


class NormalStone(ThrowWeapon):

    damage = NORMAL_STONE_DAMAGE
    attack_range = NORMAL_STONE_ATTACK_RANGE
    active_duration = math.ceil(
        NORMAL_STONE_ATTACK_RANGE / NORMAL_STONE_SPEED)
    cooldown_duration = NORMAL_STONE_COOLDOWN

    def __init__(
        self,
    ) -> None:
        super(NormalStone, self).__init__(
            NORMAL_STONE_SIZE,
            NORMAL_STONE_SIZE,
            NORMAL_STONE_LIFE,
            NORMAL_STONE_SPEED
        )
        self.destination: tuple[int, int] = None

    def deactivate(self):
        super().deactivate()
        self.destination = None

    def activate(self, direction_type: CardinalDirectionType = None) -> Weapon | None:
        if super().activate(direction_type):
            distance = self.speed * self.active_count
            self.destination = self.center + self.direction.get_vector() * distance
            return self
        return None

    def act(self) -> bool:
        super().act()
        self.move()
        return self.active_count > 0
