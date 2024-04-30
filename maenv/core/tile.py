import math
import pygame
from typing import Optional
from enum import IntEnum
from dataclasses import dataclass


class TileState(IntEnum):
    NORMAL = 0
    RESTRICT = 1


class Tile(pygame.Rect):

    def __init__(
        self,
        row: int,  # world grid
        col: int,
        address: int,
        size: int,
    ) -> None:
        super(Tile, self).__init__(
            col * size,
            row * size,
            size,
            size)
        self.row: int = row
        self.col: int = col
        self.address: int = address
        self.state: TileState = TileState.NORMAL

    def reset(self):
        self.state = TileState.NORMAL
