from __future__ import annotations
import pygame
import timeit
import uuid
import numpy as np
from collections import deque
from maenv.utils.colors import WHITE
from maenv.core.state import ObjectState


class GameObject(pygame.Rect):

    render_color = WHITE

    def __init__(
        self,
        center_x: int,
        center_y: int,
        width: int,
        height: int,
        life: int,
    ) -> None:
        super(GameObject, self).__init__(
            center_x - (width * 0.5),
            center_y - (height * 0.5),
            width, height)
        self.life = life
        self.generate_time: float = timeit.default_timer()
        self.uuid = uuid.uuid4()
        self.short_id = -1
        self.spawn_radius = 0
        self._states: deque[ObjectState] = deque()
        # if [2] is -1 is randomized range [0] , [1]
        self.delay_before_spawn = (0, 0, 0)

    @property
    def position(self):
        return self.centery << 16 | self.centerx

    def state_update(self, value: ObjectState):
        self._states.append(value)

    def get_states(self) -> list[ObjectState]:
        states = []
        while self._states:
            states.append(self._states.pop())
        return states

    def clear_event(self):
        self.step_event = None

    def is_respawnable(self) -> bool:
        return self.delay_before_spawn[1] <= self.delay_before_spawn[2]

    def is_randomize_delay(self):
        return self.delay_before_spawn[2] < 0

    def set_delay(self, start: int, end: int, randomize=False):
        self.delay_before_spawn = (
            start,
            end,
            -1 if randomize else 0
        )

    def set_randomize_delay(self, np_random: np.random.Generator):
        delay = np_random.integers(
            self.delay_before_spawn[0],
            self.delay_before_spawn[1])
        self.delay_before_spawn = (
            self.delay_before_spawn[0],
            self.delay_before_spawn[1],
            delay
        )

    def decrease_delay_before_spawn(self, increment=1):
        self.delay_before_spawn = (
            self.delay_before_spawn[0],
            self.delay_before_spawn[1],
            self.delay_before_spawn[2] + increment
        )

    def require_points(self) -> bool:
        return self.centerx == 0 and self.centery == 0

    def get_hit(self, damage: int):
        if self.life < 0:
            return
        self.life -= damage

    def set_short_id(self, short_id: int):
        self.short_id = short_id

    def render(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.render_color, self)

    def sync(self, target: tuple[int, int]):
        self.center = target

    def __hash__(self):
        # using id
        return self.short_id

    def __eq__(self, other: GameObject):
        return self.short_id == other.short_id


class Border(pygame.Rect):
    pass
