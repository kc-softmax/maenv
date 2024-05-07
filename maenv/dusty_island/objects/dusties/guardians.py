import maenv.utils.colors as colors
from maenv.core.actions import ControlAction
from maenv.dusty_island.objects.dusties.dusty import Dusty
from maenv.dusty_island.consts.game import Team
from maenv.dusty_island.consts.artifact import ArtifactType
from maenv.dusty_island.objects.artifact import Artifact
from maenv.dusty_island.objects.weapons.normal.stone import NormalStone
from maenv.dusty_island.objects.weapons.magic.magic_staff import MagicStaff


class Guardians(Dusty):

    render_color = colors.SKY_BLUE

    def __init__(
        self,
        agent_name: str,
    ) -> None:
        super(Guardians, self).__init__(
            agent_name
        )
        self.team: Team = Team.GUARDIANS
        self.normal_weapon = NormalStone()
        self.normal_weapon.owner_uuid = self.uuid
        self.magic_weapon = MagicStaff()
        self.artifacts.extend([
            Artifact(ArtifactType.WOLF),
            Artifact(ArtifactType.BEAR),
            Artifact(ArtifactType.TIGER),
        ])

    def handle_actions(self, action: ControlAction):
        super().handle_actions(action)
        artifact_type = None
        # match action:
        #     case ControlAction.SPECIAL_SKILL_1:
        #         artifact_type = ArtifactType.WOLF
        #     case ControlAction.SPECIAL_SKILL_2:
        #         artifact_type = ArtifactType.BEAR
        #     case ControlAction.SPECIAL_SKILL_3:
        #         pass
        #     case ControlAction.SPECIAL_SKILL_4:
        #         artifact_type = ArtifactType.TIGER
        if artifact := self.get_artifact(artifact_type):
            self.magic_weapon and self.magic_weapon.set_artifact(artifact)
