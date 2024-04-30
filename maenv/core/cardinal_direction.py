from __future__ import annotations
from enum import IntEnum
from math import cos, sin, pi
from pygame.math import Vector2


class CardinalDirectionType(IntEnum):
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

    def rotate(self, clockwise: bool) -> CardinalDirectionType:
        if clockwise:
            new_direction = CardinalDirectionType((self.value % 16) + 1)
        else:
            new_direction = CardinalDirectionType((self.value - 2) % 16 + 1)
        return new_direction


angle_map = {
    CardinalDirectionType.E: 0,
    CardinalDirectionType.ESE: pi / 8,
    CardinalDirectionType.SE: pi / 4,
    CardinalDirectionType.SSE: 3 * pi / 8,
    CardinalDirectionType.S: pi / 2,
    CardinalDirectionType.SSW: 5 * pi / 8,
    CardinalDirectionType.SW: 3 * pi / 4,
    CardinalDirectionType.WSW: 7 * pi / 8,
    CardinalDirectionType.W: pi,
    CardinalDirectionType.WNW: 9 * pi / 8,
    CardinalDirectionType.NW: 5 * pi / 4,
    CardinalDirectionType.NNW: 11 * pi / 8,
    CardinalDirectionType.N: 3 * pi / 2,
    CardinalDirectionType.NNE: 13 * pi / 8,
    CardinalDirectionType.NE: 7 * pi / 4,
    CardinalDirectionType.ENE: 15 * pi / 8,
}


class CardinalDirection:
    __direction_map = {
        direction: Vector2(round(cos(angle), 2), round(
            sin(angle), 2)).normalize()
        for direction, angle in angle_map.items()
    }
    current_direction: CardinalDirectionType = CardinalDirectionType.N
    target_direction: CardinalDirectionType = CardinalDirectionType.N

    def rotate_ip(self, clockwise: bool, count: int = 1):
        for _ in range(count):
            self.target_direction = self.target_direction.rotate(clockwise)

    def rotate(self, clockwise: bool, count: int = 1) -> CardinalDirectionType:
        direction = self.target_direction.rotate(clockwise)
        for _ in range(count):
            direction = self.target_direction.rotate(clockwise)
        return direction

    def is_align(self) -> bool:
        return self.current_direction == self.target_direction

    def set_direction(self, direction: CardinalDirectionType):
        self.current_direction = direction
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
