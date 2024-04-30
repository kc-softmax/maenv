import maenv.utils.colors as colors
from maenv.core.objects.game_object import GameObject
from maenv.core.objects.passive_object import PassiveGameObject

from maenv.dusty_island.consts.artifact import (
    ARTIFACT_SIZE,
    ArtifactType
)


class Artifact(PassiveGameObject):

    render_color = colors.RED

    def __init__(
        self,
        artifact_type: ArtifactType
    ) -> None:
        super(Artifact, self).__init__(
            [0, 0],
            ARTIFACT_SIZE,
            ARTIFACT_SIZE
        )
        self.artifact_type = artifact_type
