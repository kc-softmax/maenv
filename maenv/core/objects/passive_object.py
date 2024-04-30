from maenv.core.objects.game_object import GameObject


class PassiveGameObject(GameObject):
    """
        not movable, not actable
        like tree, item, bush
        따로 분리해둔 이유가 무엇일까?  
        이유를 찾아야 한다.
    """

    def __init__(
        self,
        center: tuple[int, int],
        width: int,
        height: int,
        life=1,
    ) -> None:
        super(PassiveGameObject, self).__init__(
            center[0],
            center[1],
            width,
            height,
            life)
