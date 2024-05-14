from __future__ import annotations
from maenv.dusty_island.objects.weapons import Weapon
from maenv.dusty_island.consts.axe import (
    NORMAL_AXE_SIZE,
    NORMAL_AXE_SWING_ATTACK_RANGE,
    NORMAL_AXE_SWING_DAMAGE,
    NORMAL_AXE_THROW_DAMAGE,
    NORMAL_AXE_SWING_DURATION,
    NORMAL_AXE_THROW_DURATION,
    NORMAL_AXE_COOLDOWN,
    NORMAL_AXE_ACTIVE_LIFE,
    NORMAL_AXE_SWING_ANGLE,
    NORMAL_AXE_MIN_THROW_SPEED,
    NORMAL_AXE_MAX_THROW_POWER,
    NORMAL_AXE_KNOCKBACK_POWER
)


class NormalAxe(Weapon):

    swing_attack_range = NORMAL_AXE_SWING_ATTACK_RANGE
    swing_angle = NORMAL_AXE_SWING_ANGLE

    swing_active_duration = NORMAL_AXE_SWING_DURATION
    throw_active_duration = NORMAL_AXE_THROW_DURATION
    cooldown_duration = NORMAL_AXE_COOLDOWN

    knockback_power = NORMAL_AXE_KNOCKBACK_POWER
    max_power_gauge = NORMAL_AXE_MAX_THROW_POWER
    min_throw_speed = NORMAL_AXE_MIN_THROW_SPEED
    active_life = NORMAL_AXE_ACTIVE_LIFE

    def __init__(
        self,
    ) -> None:
        super(NormalAxe, self).__init__(
            NORMAL_AXE_SIZE,
            NORMAL_AXE_SIZE,
        )

    def get_damage(self) -> int:
        if self.throwing:
            return NORMAL_AXE_THROW_DAMAGE
        else:
            return NORMAL_AXE_SWING_DAMAGE
