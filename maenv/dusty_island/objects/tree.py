import maenv.utils.colors as colors
from maenv.dusty_island.consts.tree import (
    DEFAULT_TREE_SIZE,
    DEFAULT_TREE_LIFE
)
from maenv.core.objects.passive_object import PassiveGameObject


class Tree(PassiveGameObject):

    render_color = colors.GREEN

    def __init__(
        self,
    ) -> None:
        # tree Type에 따라 변경
        super(Tree, self).__init__(
            [0, 0],
            DEFAULT_TREE_SIZE,
            DEFAULT_TREE_SIZE,
            DEFAULT_TREE_LIFE
        )


class TrimmedTree(PassiveGameObject):

    render_color = colors.GRAY

    def __init__(
        self,
        point: tuple[int, int]
    ) -> None:
        # tree Type에 따라 변경
        super(TrimmedTree, self).__init__(
            point,
            DEFAULT_TREE_SIZE,
            DEFAULT_TREE_SIZE,
            DEFAULT_TREE_LIFE
        )
        self.impenetrability = True
