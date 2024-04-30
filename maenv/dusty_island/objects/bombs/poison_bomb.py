import pygame
import maenv.utils.colors as colors
from maenv.core.cardinal_direction import CardinalDirectionType
from maenv.dusty_island.consts.bombs import (
    POISION_BOMB_TICK_DAMAGE,
    POISION_BOMB_EXPLOSION_SIZE,
    POISION_BOMB_MIN_THROW_RANGE,
    POISION_BOMB_MAX_THROW_RANGE,
    POISION_BOMB_HITTING_COOLDOWN,
    POISION_BOMB_DELAY_COOLDOWN,
    POISION_BOMB_ACTIVE_DURATION,
)
from maenv.dusty_island.objects.bombs import Bomb


class PoisionBomb(Bomb):

    damage = POISION_BOMB_TICK_DAMAGE
    hitting_cooldown = POISION_BOMB_HITTING_COOLDOWN
    delay_cooldown = POISION_BOMB_DELAY_COOLDOWN
    active_duration = POISION_BOMB_ACTIVE_DURATION
    min_range = POISION_BOMB_MIN_THROW_RANGE
    max_range = POISION_BOMB_MAX_THROW_RANGE

    def __init__(
        self,
        center: tuple[int, int],
        bomber_id: int,
        throw_gauge: float,
        direction_type: CardinalDirectionType
    ) -> None:
        super(PoisionBomb, self).__init__(
            center,
            POISION_BOMB_EXPLOSION_SIZE,
            bomber_id,
            throw_gauge,
            direction_type
        )

    def render(self, surface: pygame.Surface):
        if self.delay_count > 0:
            pygame.draw.rect(surface, colors.ORANGE, self)
        elif self.active_count > 0:
            pygame.draw.rect(surface, colors.GREEN, self)
        else:
            pygame.draw.rect(surface, self.render_color, self)
