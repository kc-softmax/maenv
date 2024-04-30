import pygame
import maenv.utils.colors as colors
from maenv.core.cardinal_direction import CardinalDirectionType
from maenv.dusty_island.consts.bombs import (
    FIRE_BOMB_TICK_DAMAGE,
    FIRE_BOMB_ACTIVE_DURATION,
    FIRE_BOMB_DELAY_COOLDOWN,
    FIRE_BOMB_EXPLOSION_SIZE,
    FIRE_BOMB_HITTING_COOLDOWN,
    FIRE_BOMB_MIN_THROW_RANGE,
    FIRE_BOMB_MAX_THROW_RANGE
)
from maenv.dusty_island.objects.bombs import Bomb


class FireBomb(Bomb):

    damage = FIRE_BOMB_TICK_DAMAGE
    hitting_cooldown = FIRE_BOMB_HITTING_COOLDOWN
    delay_cooldown = FIRE_BOMB_DELAY_COOLDOWN
    active_duration = FIRE_BOMB_ACTIVE_DURATION
    min_range = FIRE_BOMB_MIN_THROW_RANGE
    max_range = FIRE_BOMB_MAX_THROW_RANGE

    def __init__(
        self,
        center: tuple[int, int],
        bomber_id: int,
        throw_gauge: float,
        direction_type: CardinalDirectionType
    ) -> None:
        super(FireBomb, self).__init__(
            center,
            FIRE_BOMB_EXPLOSION_SIZE,
            bomber_id,
            throw_gauge,
            direction_type
        )

    def render(self, surface: pygame.Surface):
        if self.delay_count > 0:
            pygame.draw.rect(surface, colors.PURPLE, self)
        elif self.active_count > 0:
            pygame.draw.rect(surface, colors.CRIMSON, self)
        else:
            pygame.draw.rect(surface, self.render_color, self)
