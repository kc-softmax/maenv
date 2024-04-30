import math
import pygame
from maenv.utils.colors import (
    BETA_GRID,
    BLACK
)
from maenv.core.maenv import MaEnv
from maenv.core.actions import ControlAction
from maenv.core.tile import TileState, Tile
from maenv.core.state import ObjectState
from maenv.core.objects.game_object import GameObject
from maenv.core.objects.active_object import ActiveGameObject
from maenv.core.objects.passive_object import PassiveGameObject
from maenv.core.objects.collision_object import CollisionObject
from maenv.dusty_island.consts.game import (
    MAX_AGENTS,
    ARTIFACT_RATIO,
    TREE_RATIO,
    MAX_ARTIFACT_COUNT_AT_ONCE,
    Team,
)
from maenv.dusty_island.consts.artifact import ArtifactType
from maenv.dusty_island.objects.tree import Tree
from maenv.dusty_island.objects.dusties.dusty import Dusty
from maenv.dusty_island.objects.dusties.colonists import Colonists
from maenv.dusty_island.objects.dusties.guardians import Guardians
from maenv.dusty_island.objects.artifact import Artifact
from maenv.dusty_island.maps.default_map import DefaultMap
from maenv.dusty_island.objects.weapons.normal.axe import NormalAxe
from maenv.dusty_island.objects.weapons.normal.stone import NormalStone
from maenv.dusty_island.objects.bombs import Bomb
from maenv.dusty_island.objects.summons import (
    Summon,
)


class DustyEnv(MaEnv):

    def __init__(
        self,
        agent_names: list[str] = [],
    ) -> None:
        super().__init__()
        self.map = DefaultMap()
        self.summons: dict[int, Summon] = {}
        self.agents: dict[int, Dusty] = {}
        self.artifcats: dict[int, Artifact] = {}
        self.artifact_count = math.floor(MAX_AGENTS * ARTIFACT_RATIO)
        self.tree_count = math.floor(MAX_AGENTS * TREE_RATIO)
        self.removed_tree = 0
        self.pending_spawn_objects.extend(
            [Tree() for _ in range(self.tree_count)])
        assert len(agent_names) < MAX_AGENTS
        for i, agent_name in enumerate(agent_names):
            team = Team.COLONISTS if i % 2 == 0 else Team.GUARDIANS
            self._generate_dusty(agent_name, team)

    def reset(self, seed: int):
        super().reset(seed=seed)

    def render(self, display_width: int, display_height: int) -> pygame.Surface:

        surface: pygame.Surface = pygame.Surface(
            (self.map.map_width, self.map.map_height)
        )
        surface.fill(BLACK)

        for tile in self.map.tile_map.values():
            if tile.state == TileState.RESTRICT:
                pygame.draw.rect(surface, BETA_GRID, tile)

        for game_object in self.game_objects.values():
            game_object.render(surface)

        for agent in self.agents.values():
            pygame.draw.line(
                surface, agent.render_color,
                agent.center, agent.center + agent.direction.get_vector() * 32, 10)

        return pygame.transform.scale(
            surface, (display_width, display_height))

    def _generate_dusty(self, agent_name: str, team: Team = None) -> Dusty:
        if team is None:
            colonists = len(
                [agent for agent in self.agents.values() if agent.team == Team.COLONISTS])
            guardians = len(
                [agent for agent in self.agents.values() if agent.team == Team.GUARDIANS])
            selected_team = Team.GUARDIANS if guardians > colonists else Team.COLONISTS
        else:
            selected_team = team
        if selected_team == Team.COLONISTS:
            dusty = Colonists(agent_name)
        else:
            dusty = Guardians(agent_name)

        self.pending_spawn_objects.append(dusty)
        return dusty

    def _remove_dusty(self, dusty: Dusty):
        self.removing_game_object_ids.append(dusty.short_id)

    def _respawn_artifacts(self):

        new_artifact_count = self.artifact_count - len(self.artifcats)

        if new_artifact_count > MAX_ARTIFACT_COUNT_AT_ONCE:
            new_artifact_count = MAX_ARTIFACT_COUNT_AT_ONCE

        artifact_types = ArtifactType.get_random_type(
            self.np_random, new_artifact_count)

        self.pending_spawn_objects.extend(
            [Artifact(artifact_types[i]) for i in range(new_artifact_count)])

    def _handle_register_object(self, game_object: GameObject):
        super()._handle_register_object(game_object)
        if isinstance(game_object, Dusty):
            self.agents[game_object.short_id] = game_object
        elif isinstance(game_object, Artifact):
            self.artifcats[game_object.short_id] = game_object
        elif isinstance(game_object, Summon):
            self.summons[game_object.short_id] = game_object
        elif isinstance(game_object, Tree):
            self.map.update_tile_state(
                self.map.get_tile_address(
                    game_object.centerx, game_object.centery),
                TileState.RESTRICT
            )

    def _handle_remove_object(self, game_object: GameObject):
        super()._handle_remove_object(game_object)
        if isinstance(game_object, Dusty):
            del self.agents[game_object.short_id]
        elif isinstance(game_object, Summon):
            del self.summons[game_object.short_id]
        elif isinstance(game_object, Artifact):
            del self.artifcats[game_object.short_id]
        elif isinstance(game_object, Tree):
            self.map.update_tile_state(
                self.map.get_tile_address(
                    game_object.centerx, game_object.centery),
                TileState.NORMAL
            )
            self.removed_tree += 1

    def _handle_collision_object(self, src: GameObject, other: GameObject):
        src_destory = False
        other_destory = False
        if isinstance(src, Dusty):
            if (
                isinstance(other, Tree) or
                isinstance(other, CollisionObject) or
                isinstance(other, Dusty)
            ):
                src.is_move_cancelled = True
            elif isinstance(other, Artifact):
                other_destory = src.acquire_item(other)
        elif isinstance(src, NormalAxe) and src.owner_uuid:
            if src.owner_uuid == other.uuid:
                return
            if not isinstance(other, CollisionObject):
                other.get_hit(src.damage)
                other.state_update(ObjectState.HIT)
                src.deactivate()
        elif isinstance(src, NormalStone):
            # 결국 데미지를 주냐 안주냐 차이
            # 기본적으로 stone은 부딪히면 터진다.
            # 특정 돌이 아니면?
            # shooter 와의 충돌은 무시한다.
            if isinstance(other, Dusty) and src.owner_uuid == other.uuid:
                return
            src_destory = True
            src.deactivate()
            if isinstance(other, Tree):
                pass  # 나무에게는 피해를 주지 않는다.
            else:
                other.get_hit(src.damage)
        elif isinstance(src, Bomb):
            if not src.is_activate():
                return
            if src.hit(other.short_id):
                other.get_hit(src.damage)

        src_destory and self.removing_game_object_ids.append(
            src.short_id)

        other_destory and self.removing_game_object_ids.append(
            other.short_id)

    def _step_processing(self, actions: dict[int | str, list[ControlAction]]):
        super()._step_processing(actions)
        for summon in self.summons.values():
            summon.state_update(ObjectState.MOVING)

        for agent in self.agents.values():
            while agent.pending_weapons:
                self.pending_spawn_objects.append(agent.pending_weapons.pop())
            agent.state_update(ObjectState.MOVING)
            if agent.normal_weapon.is_activate():
                agent.normal_weapon.state_update(ObjectState.MOVING)

    def _post_step_processing(self):
        super()._post_step_processing()
        for agent in self.agents.values():
            if agent.is_move_cancelled:
                agent.cancel_movement()
        self._respawn_artifacts()

    def _get_terminateds(self) -> dict[str, bool]:
        """
        Returns whether each agent is terminated or not.
        TODO set terminate condition
        TODO select a winner if the game is terminated
        currently, agent is terminated when max_steps is reached        
        """
        terminated: dict[int, bool] = {
            agent_id: False for agent_id in self.agents
        }

        terminated['__all__'] = self.tree_count == self.removed_tree

        return terminated
