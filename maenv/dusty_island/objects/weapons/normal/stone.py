from maenv.dusty_island.objects.weapons import ThrowWeapon
from maenv.dusty_island.consts.weapons.normal_weapons import (
    NORMAL_STONE_DAMAGE,
    NORMAL_STONE_COOLDOWN,
    NORMAL_STONE_LIFE,
    NORMAL_STONE_SIZE,
    NORMAL_STONE_DURATION,
    NORMAL_STONE_MIN_SPEED,
    NORMAL_STONE_MAX_POWER,
    NORMAL_STONE_TARGETING_RANGE,
    NORMAL_STONE_TARGETING_ANGLE
)
from maenv.dusty_island.objects.weapons.weapons import Weapon


class NormalStone(ThrowWeapon):

    damage = NORMAL_STONE_DAMAGE
    targeting_angle = NORMAL_STONE_TARGETING_ANGLE
    targeting_range = NORMAL_STONE_TARGETING_RANGE
    max_power_gauge = NORMAL_STONE_MAX_POWER
    active_duration = NORMAL_STONE_DURATION
    cooldown_duration = NORMAL_STONE_COOLDOWN

    def __init__(
        self,
    ) -> None:
        super(NormalStone, self).__init__(
            NORMAL_STONE_SIZE,
            NORMAL_STONE_SIZE,
            NORMAL_STONE_LIFE,
            NORMAL_STONE_MIN_SPEED
        )
