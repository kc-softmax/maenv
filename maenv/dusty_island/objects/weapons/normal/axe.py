import math
from maenv.dusty_island.consts.weapons.normal_weapons import (
    NORMAL_AXE_ATTACK_RANGE,
    NORMAL_AXE_COOLDOWN,
    NORMAL_AXE_DAMAGE,
    NORMAL_AXE_DURATION,
    NORMAL_AXE_LIFE,
    NORMAL_AXE_SIZE,
    NORMAL_AXE_SWING_ANGLE
)
from maenv.dusty_island.objects.weapons import Weapon


class NormalAxe(Weapon):

    damage = NORMAL_AXE_DAMAGE
    attack_range = NORMAL_AXE_ATTACK_RANGE
    active_duration = NORMAL_AXE_DURATION
    cooldown_duration = NORMAL_AXE_COOLDOWN

    def __init__(
        self,
    ) -> None:
        super(NormalAxe, self).__init__(
            NORMAL_AXE_SIZE,
            NORMAL_AXE_SIZE,
            NORMAL_AXE_LIFE,
        )

    def get_next_position(self) -> tuple[int, int]:
        progress = self.active_gauge / NORMAL_AXE_DURATION
        axe_direction = self.direction.get_vector().rotate(
            NORMAL_AXE_SWING_ANGLE / 2 - NORMAL_AXE_SWING_ANGLE * progress
        ).normalize()
        # 원의 방정식을 사용하여 x, y 좌표 계산
        offset_x = self.width * 0.5 + self.attack_range
        offset_y = self.height * 0.5 + self.attack_range

        return [
            math.floor(self.centerx + offset_x * axe_direction.x),
            math.floor(self.centery + offset_y * axe_direction.y)
        ]

    def act(self):
        super().act()
        self.center = self.get_next_position()
