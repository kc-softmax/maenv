import maenv.utils.colors as colors
from maenv.core.objects.active_object import ActiveGameObject
from maenv.core.cardinal_direction import CardinalDirection
from maenv.dusty_island.consts.artifact import ArtifactType
from maenv.dusty_island.consts.summon import (
    SummonState,
    WOLF_DAMAGE,
    WOLF_LIFE,
    WOLF_SIZE,
    WOLF_SPEED,
    BEAR_DAMAGE,
    BEAR_LIFE,
    BEAR_SIZE,
    BEAR_SPEED,
    TIGER_DAMAGE,
    TIGER_LIFE,
    TIGER_SIZE,
    TIGER_SPEED
)


class Summon(ActiveGameObject):

    damage = None
    summon_type = None
    direction_system = CardinalDirection

    def __init__(
        self,
        center: tuple[int, int],
        size: int,
        life: int,
        speed: int,
        summoner: int,
    ) -> None:
        super(Summon, self).__init__(
            center[0],
            center[1],
            size,
            size,
            life,
            speed,
        )
        self.summoner = summoner
        self.state = SummonState.IDLE

    def act(self) -> bool:
        super().act()
        # 주로 이동을 담당한다?
        # self.move()
        return True


class Wolf(Summon):

    render_color = colors.BLUE
    damage = WOLF_DAMAGE
    summon_type = ArtifactType.WOLF

    def __init__(
        self,
        center: tuple[int, int],
        summoner: int,
    ) -> None:
        super(Wolf, self).__init__(
            center,
            WOLF_SIZE,
            WOLF_LIFE,
            WOLF_SPEED,
            summoner
        )


class Bear(Summon):

    damage = BEAR_DAMAGE
    summon_type = ArtifactType.BEAR

    def __init__(
        self,
        center: tuple[int, int],
        summoner: int,
    ) -> None:
        super(Bear, self).__init__(
            center,
            BEAR_SIZE,
            BEAR_LIFE,
            BEAR_SPEED,
            summoner
        )


class Tiger(Summon):

    damage = TIGER_DAMAGE
    summon_type = ArtifactType.TIGER

    def __init__(
        self,
        center: tuple[int, int],
        summoner: int,
    ) -> None:
        super(Tiger, self).__init__(
            center,
            TIGER_SIZE,
            TIGER_LIFE,
            TIGER_SPEED,
            summoner
        )
