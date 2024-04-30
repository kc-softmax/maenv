import maenv.utils.colors as colors
from maenv.core.actions import ControlAction
from maenv.dusty_island.objects.dusties.dusty import Dusty
from maenv.dusty_island.consts.game import Team
from maenv.dusty_island.consts.artifact import ArtifactType
from maenv.dusty_island.objects.artifact import Artifact
from maenv.dusty_island.objects.weapons.normal.axe import NormalAxe
from maenv.dusty_island.objects.weapons.magic.magic_gun import MagicGun


class Colonists(Dusty):

    render_color = colors.CRIMSON

    def __init__(
        self,
        agent_name: str,
    ) -> None:
        super(Colonists, self).__init__(
            agent_name
        )
        self.team: Team = Team.COLONISTS
        self.normal_weapon = NormalAxe()
        self.normal_weapon.owner_uuid = self.uuid
        self.normal_weapon.follow_direction(self.direction)
        self.magic_weapon = MagicGun()
        self.magic_weapon.follow_direction(self.direction)
        self.artifacts.extend([
            Artifact(ArtifactType.SHOTGUN),
            Artifact(ArtifactType.SHOTGUN),
            Artifact(ArtifactType.SHOTGUN),
            Artifact(ArtifactType.SHOTGUN),
            Artifact(ArtifactType.POISON_BOMB),
            Artifact(ArtifactType.BUSTER_CALL),
        ])

    def handle_actions(self, action: ControlAction):
        super().handle_actions(action)
        artifact_type = None
        match action:
            case ControlAction.SPECIAL_SKILL_1:
                artifact_type = ArtifactType.SHOTGUN
            case ControlAction.SPECIAL_SKILL_2:
                artifact_type = ArtifactType.POISON_BOMB
            case ControlAction.SPECIAL_SKILL_3:
                pass
                # artifact_type = WeaponType.POTION
            case ControlAction.SPECIAL_SKILL_4:
                artifact_type = ArtifactType.BUSTER_CALL

        if artifact := self.get_artifact(artifact_type):
            self.magic_weapon and self.magic_weapon.set_artifact(artifact)
