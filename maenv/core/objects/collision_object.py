from maenv.core.objects.game_object import GameObject
from enum import IntEnum


class CollisionObjectType(IntEnum):
    TILE = 1


class CollisionObject(GameObject):

    collision_type = CollisionObjectType.TILE

    def __init__(
        self,
        center,
        width: int,
        height: int,
    ) -> None:
        super(CollisionObject, self).__init__(
            center[0],
            center[1],
            width,
            height,
            -1)
