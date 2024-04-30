import math
from maenv.dusty_island.objects.weapons import ThrowWeapon
from maenv.dusty_island.consts.weapons.normal_weapons import (
    NORMAL_STONE_DAMAGE,
    NORMAL_STONE_ATTACK_RANGE,
    NORMAL_STONE_COOLDOWN,
    NORMAL_STONE_LIFE,
    NORMAL_STONE_SIZE,
    NORMAL_STONE_SPEED,
)


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

    def act(self) -> bool:
        super().act()
        self.move()
        return self.active_count > 0
