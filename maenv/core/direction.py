from __future__ import annotations
from enum import IntEnum
from math import cos, sin, pi
from pygame.math import Vector2


class DirectionType(IntEnum):
    NNE = 1
    NE = 2
    ENE = 3
    E = 4
    ESE = 5
    SE = 6
    SSE = 7
    S = 8
    SSW = 9
    SW = 10
    WSW = 11
    W = 12
    WNW = 13
    NW = 14
    NNW = 15
    N = 16

    def rotate(self, clockwise: bool) -> DirectionType:
        if clockwise:
            new_direction = DirectionType((self.value % 16) + 1)
        else:
            new_direction = DirectionType((self.value - 2) % 16 + 1)
        return new_direction


angle_map = {
    DirectionType.E: 0,
    DirectionType.ESE: pi / 8,
    DirectionType.SE: pi / 4,
    DirectionType.SSE: 3 * pi / 8,
    DirectionType.S: pi / 2,
    DirectionType.SSW: 5 * pi / 8,
    DirectionType.SW: 3 * pi / 4,
    DirectionType.WSW: 7 * pi / 8,
    DirectionType.W: pi,
    DirectionType.WNW: 9 * pi / 8,
    DirectionType.NW: 5 * pi / 4,
    DirectionType.NNW: 11 * pi / 8,
    DirectionType.N: 3 * pi / 2,
    DirectionType.NNE: 13 * pi / 8,
    DirectionType.NE: 7 * pi / 4,
    DirectionType.ENE: 15 * pi / 8,
}


class Direction:
    __direction_map = {
        direction: Vector2(round(cos(angle), 2), round(
            sin(angle), 2)).normalize()
        for direction, angle in angle_map.items()
    }
    current_direction: DirectionType = DirectionType.N
    _target_direction: DirectionType = DirectionType.N

    @property
    def target_direction(self):
        return self._target_direction

    @target_direction.setter
    def target_direction(self, value: DirectionType):
        if not isinstance(value, DirectionType):
            raise ValueError(
                "target_direction must be an instance of DirectionType Enum")
        self._target_direction = value
        if not self.is_wheel_mode:
            self.current_direction = value

    def __init__(self, is_wheel_mode=False) -> None:
        self.is_wheel_mode = is_wheel_mode
        self._target_direction: DirectionType = DirectionType.N

    def rotate_ip(self, clockwise: bool, count: int = 1):
        for _ in range(count):
            self.target_direction = self.target_direction.rotate(clockwise)

    def rotate(self, clockwise: bool, count: int = 1) -> DirectionType:
        direction = self.target_direction.rotate(clockwise)
        for _ in range(count):
            direction = self.target_direction.rotate(clockwise)
        return direction

    def is_align(self) -> bool:
        return self.current_direction == self.target_direction

    def set_direction(self, direction: DirectionType):
        self.target_direction = direction

    def get_vector(self) -> Vector2:
        return self.__direction_map[self.current_direction]

    def update(self):
        if self.current_direction == self.target_direction:
            return
        diff = (self.target_direction.value -
                self.current_direction.value) % 16
        clockwise = True if diff <= 8 else False
        self.current_direction = self.current_direction.rotate(clockwise)
