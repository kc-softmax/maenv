import maenv.utils.colors as colors
from maenv.dusty_island.objects.weapons.magic import MagicWeapon
from maenv.dusty_island.consts.artifact import (
    ArtifactType
)
from maenv.dusty_island.consts.weapons.magic_weapons import (
    MAGIC_STAFF_COOLDOWN,
)
from maenv.dusty_island.objects.bullets import Bullet


class MagicStaff(MagicWeapon):

    render_color = colors.CRIMSON
    cooldown_duration = MAGIC_STAFF_COOLDOWN
    equippable_artifacts_type = [
        ArtifactType.WOLF, ArtifactType.BEAR, ArtifactType.TIGER
    ]

    def __init__(
        self,
    ) -> None:
        super(MagicStaff, self).__init__()

    def activate_artifact(self) -> list[Bullet]:
        match self.artifact.artifact_type:
            case ArtifactType.WOLF:
                pass
            case ArtifactType.BEAR:
                pass
            case ArtifactType.TIGER:
                pass
