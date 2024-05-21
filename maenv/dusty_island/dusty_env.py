import math
import pygame
from maenv.utils.colors import (
    BETA_GRID,
    BLACK,
    CRIMSON
)
from maenv.core.maenv import MaEnv
from maenv.core.actions import ControlAction
from maenv.core.tile import TileState
from maenv.core.state import ObjectState
from maenv.core.objects.game_object import GameObject
from maenv.core.objects.collision_object import CollisionObject
from maenv.dusty_island.consts.actions import DustyCastingType
from maenv.dusty_island.maps.default_map import DefaultMap
from maenv.dusty_island.objects.trees import Tree, TrimmedTree
from maenv.dusty_island.objects.dusties.dusty import Dusty
from maenv.dusty_island.objects.bombs import Bomb
from maenv.dusty_island.objects.weapons import Weapon, NormalAxe
from maenv.dusty_island.objects.items import UnOwnedWeapon
from maenv.dusty_island.consts.game import (
    MAX_AGENTS,
    TREE_RATIO,
)


class DustyEnv(MaEnv):

    def __init__(
        self,
        agent_names: list[str] = [],
    ) -> None:
        super().__init__()
        self.map = DefaultMap()
        self.agents: dict[int, Dusty] = {}
        self.throwing_weapons: dict[int: Weapon] = {}
        self.tree_count = math.floor(MAX_AGENTS * TREE_RATIO)
        self.removed_tree = 0
        self.pending_spawn_objects.extend(
            [Tree() for _ in range(self.tree_count)])
        assert len(agent_names) < MAX_AGENTS
        for agent_name in agent_names:
            self._generate_dusty(agent_name)

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
            if agent.weapon and agent.weapon.preparing:
                pygame.draw.line(
                    surface, CRIMSON,
                    agent.center, agent.center + agent.aiming_vector * 32, 10)

        return pygame.transform.scale(
            surface, (display_width, display_height))

    def _generate_dusty(self, agent_name: str) -> Dusty:
        dusty = Dusty(agent_name)

        self.pending_spawn_objects.append(dusty)
        return dusty

    def _remove_dusty(self, dusty: Dusty):
        self.removing_game_object_ids.append(dusty.short_id)

    def _handle_register_object(self, game_object: GameObject):
        super()._handle_register_object(game_object)
        if isinstance(game_object, Dusty):
            self.agents[game_object.short_id] = game_object
            game_object.pickup_weapon(NormalAxe())
        elif isinstance(game_object, Weapon):
            if game_object.throwing:
                self.throwing_weapons[game_object.short_id] = game_object
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
        elif isinstance(game_object, Tree):
            self.pending_spawn_objects.append(
                TrimmedTree(game_object.center)
            )
            self.removed_tree += 1
        elif isinstance(game_object, Weapon):
            if game_object.throwing:
                if game_object.throw_limit != 0:
                    # -1 is infinity
                    # 방향도
                    self.pending_spawn_objects.append(
                        UnOwnedWeapon(
                            width=game_object.width,
                            height=game_object.height,
                            throw_limit=game_object.throw_limit,
                            weapon_cls=type(game_object),
                            center=(game_object.centerx, game_object.centery),
                            is_facing_right=game_object.direction.get_vector().x > 0
                        )
                    )
                    self.throwing_weapons.pop(game_object.short_id)
        elif isinstance(game_object, UnOwnedWeapon):
            if owner := self.agents.get(game_object.owner_id):
                # generate weapon and attach dusty:
                owner.pickup_weapon(game_object.activate_weapon())

    def _handle_collision_object(self, src: GameObject, other: GameObject):
        src_destory = False
        other_destory = False
        if isinstance(src, Dusty):
            if (
                isinstance(other, Tree) or
                isinstance(other, TrimmedTree) or
                isinstance(other, CollisionObject) or
                isinstance(other, Dusty)
            ):
                src.is_move_cancelled = True
            elif isinstance(other, UnOwnedWeapon):
                other.collide_with_dusty(src.short_id)
        elif isinstance(src, Weapon) and src.owner_id:
            if src.owner_id == other.short_id:
                return
            if isinstance(other, TrimmedTree):
                # 음 어떻게 해야할까
                return
            if isinstance(other, CollisionObject):
                return

            if isinstance(other, Weapon) and src.owner_id == other.owner_id:
                return
            if other.get_hit(src.get_damage()):
                src.get_hit(src.get_damage())
                self._add_hit_event(src, other)
                if isinstance(other, Dusty):
                    other.update_state(
                        ObjectState.KNOCKBACK,
                        target=src,
                        value=src.knockback_power
                    )

        elif isinstance(src, Bomb):
            if not src.is_activate():
                return
            if other.get_hit(src.damage):
                # src.hit(other.short_id):
                # other.get_hit(src.damage)
                self._add_hit_event(src, other)

        src_destory and self.removing_game_object_ids.append(
            src.short_id)

        other_destory and self.removing_game_object_ids.append(
            other.short_id)

    def _add_hit_event(self, src: GameObject, target: GameObject):
        src.update_state(
            state=ObjectState.HITTING,
            target=target,
        )
        target.update_state(
            state=ObjectState.DAMAGED,
            target=src,
        )

    def _add_moving_event(sef, src: GameObject):
        src.update_state(
            state=ObjectState.MOVING,
            value=src.position
        )

    def _step_processing(self, actions: dict[int | str, list[ControlAction]]):
        super()._step_processing(actions)

        for throwing_weapon in self.throwing_weapons.values():
            self._add_moving_event(throwing_weapon)

        for agent in self.agents.values():
            while agent.pending_weapons:
                weapon = agent.pending_weapons.pop()
                if weapon.throwing:
                    agent.release_weapon()
                    casting_type = DustyCastingType.THROW_WEAPON
                else:
                    casting_type = DustyCastingType.SWING_WEAPON
                agent.update_state(
                    ObjectState.CASTING,
                    value=casting_type)
                self.pending_spawn_objects.append(weapon)

            if not agent.is_move_cancelled and agent.moved:
                self._add_moving_event(agent)
            else:
                # 무조건 하나는 넣는다. 규칙을 정해서 해야한다.
                agent.update_state(ObjectState.IDLE)

    def _post_step_processing(self):
        super()._post_step_processing()
        for agent in self.agents.values():
            if agent.is_move_cancelled:
                agent.cancel_movement()

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
