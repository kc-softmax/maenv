from maenv.core.objects.game_object import GameObject
from enum import IntEnum


class CollisionObjectType(IntEnum):
    TILE = 1


class CollisionObject(GameObject):
    """
        현재는 타일과 충돌시 발생하는 object
        1회용이다.
    """

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
