
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
            0
        )

    def act(self) -> bool:
        super().act()
        if self.active_count > 0:
            progress = self.active_count / NORMAL_AXE_DURATION
            axe_direction = self.direction.get_vector().rotate(
                NORMAL_AXE_SWING_ANGLE / 2 - NORMAL_AXE_SWING_ANGLE * progress
            ).normalize()
            # 원의 방정식을 사용하여 x, y 좌표 계산
            offset_x = self.width * 0.5 + self.attack_range
            offset_y = self.height * 0.5 + self.attack_range

            self.centerx += offset_x * axe_direction.x
            self.centery += offset_y * axe_direction.y
            self.active_count -= 1

        return self.active_count > 0
