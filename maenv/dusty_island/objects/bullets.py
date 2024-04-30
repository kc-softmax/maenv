import math
from maenv.core.objects.active_object import ActiveGameObject
from maenv.dusty_island.consts.bullets import (
    DEFAULT_BULLET_ATTACK_RANGE,
    DEFAULT_BULLET_DAMAGE,
    DEFAULT_BULLET_LIFE,
    DEFAULT_BULLET_SIZE,
    DEFAULT_BULLET_SPEED

)


class Bullet(ActiveGameObject):

    damage = DEFAULT_BULLET_DAMAGE
    attack_range = DEFAULT_BULLET_ATTACK_RANGE

    bullet_size = DEFAULT_BULLET_SIZE
    bullet_life = DEFAULT_BULLET_LIFE
    bullet_speed = DEFAULT_BULLET_SPEED

    def __init__(
        self,
        center: tuple[int, int],
        shooter_id: int,
    ) -> None:
        super(Bullet, self).__init__(
            center,
            self.bullet_size,
            self.bullet_size,
            self.bullet_life,
            self.bullet_speed,
        )
        self.shooter_id = shooter_id
        self.active_count = math.ceil(self.attack_range / self.speed)

    def act(self) -> bool:
        self.active_count -= 1
        self.move()
        return self.active_count > 0
