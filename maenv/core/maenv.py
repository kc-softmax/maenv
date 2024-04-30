from maenv.core.tile_map import TileMap, Tile
from maenv.core.objects.active_object import ActiveGameObject
from maenv.core.objects.collision_object import CollisionObject
from maenv.core.objects.passive_object import PassiveGameObject
from maenv.core.objects.game_object import GameObject
from maenv.core.actions import ControlAction
from maenv.core.state import ObjectState
from maenv.core.id_manager import IDManager
import collections
import gymnasium as gym
from warnings import warn
from maenv.utils import randomize_center


class MaEnv(gym.Env):

    def __init__(
        self,
    ) -> None:
        super(MaEnv, self).__init__()

        self.id_manager = IDManager()
        self.game_objects: dict[int: GameObject] = {}
        self.removing_game_object_ids: list[int] = []
        self.pending_spawn_objects: list[GameObject] = []
        self.step_count = 0
        self.map: TileMap = TileMap(30, 30, 32)
        self.passive_address_map: dict[int: list[GameObject]] = collections.defaultdict(
            list)

    def reset(self, seed: int):
        super().reset(seed=seed)
        self.step_count = 0

    def step(self, actions: dict[int | str, list[ControlAction]]):
        self._step_processing(actions)
        address_map = self._get_address_map()
        self.map.update_respawn_addresses(address_map.keys())
        collisions = self._check_collisions(address_map)
        while collisions:
            self._handle_collision_object(*collisions.pop())
        self._post_step_processing()
        self._update_state_of_objects()
        self._register_game_objects()
        self._remove_objects()

        obs = self._get_observations()
        rewards = self._get_rewards()
        infos = self._get_infos()
        truncateds = self._get_truncateds()
        terminateds = self._get_terminateds()
        self.step_count += 1
        return obs, rewards, terminateds, truncateds, infos

    def _get_address_map(self) -> dict[int: list[GameObject]]:
        address_map: dict[int: list[GameObject]
                          ] = self.passive_address_map.copy()
        for game_object in self.game_objects.values():
            if not isinstance(game_object, ActiveGameObject):
                continue
            address = self.map.get_tile_address(
                game_object.centerx, game_object.centery)
            address_map[address].append(game_object)
        return address_map

    def _check_collisions(self, address_map: dict[int: list[GameObject]]) -> collections.deque[
            tuple[GameObject, GameObject]]:

        collisions: collections.deque[
            tuple[GameObject, GameObject]] = collections.deque()
        for game_object in self.game_objects.values():
            if not isinstance(game_object, ActiveGameObject):
                continue

            neighbors_addresses = self.map.get_neighbor_addresses(
                game_object.centerx, game_object.centery)
            for address in neighbors_addresses:
                addressed_objects = address_map[address]

                if address in self.map.restrict_addresses:
                    restrcit_tile: Tile = self.map.tile_map[address]
                    if game_object.colliderect(restrcit_tile):
                        collisions.append((game_object, CollisionObject(
                            restrcit_tile.center,
                            restrcit_tile.width,
                            restrcit_tile.height,
                        )))
                for addressed_object in addressed_objects:
                    if game_object == addressed_object:
                        continue
                    if game_object.colliderect(addressed_object):
                        collisions.append((game_object, addressed_object))
        return collisions

    def _handle_collision_object(self, src: GameObject, other: GameObject):
        pass

    def _get_observations(self) -> dict[str, any]:
        return {}

    def _get_rewards(self) -> dict[str, any]:
        return {}

    def _get_infos(self) -> dict[str, any]:
        return {}

    def _get_initial_infos(self) -> dict[str, any]:
        return {}

    def _get_terminateds(self) -> dict[str, bool]:
        return {}

    def _get_truncateds(self) -> dict[str, bool]:
        return {}

    def _handle_register_object(self, game_object: GameObject):
        if isinstance(game_object, PassiveGameObject):
            address = self.map.get_tile_address(
                game_object.centerx, game_object.centery)
            if address in self.passive_address_map:
                warn('check remove passive object algorithm')
            self.passive_address_map[address].append(game_object)

    def _handle_update_object(self, game_object: ActiveGameObject, states: list[ObjectState]):
        pass

    def _handle_remove_object(self, game_object: GameObject):
        if isinstance(game_object, PassiveGameObject):
            address = self.map.get_tile_address(
                game_object.centerx, game_object.centery)
            self.passive_address_map[address].remove(game_object)
            if not self.passive_address_map[address]:
                del self.passive_address_map[address]

    def _register_game_objects(self):

        # delay가 아닌 애들 먼저
        delay_spawn_objects: list[GameObject] = []
        required_position_objects = [
            game_object
            for game_object in self.pending_spawn_objects
            if game_object.is_respawnable() and game_object.require_points()
        ]
        positions = self.map.get_respawn_positions(
            self.np_random, len(required_position_objects))
        while self.pending_spawn_objects:
            game_object = self.pending_spawn_objects.pop()
            if not game_object.is_respawnable():
                game_object.is_randomize_delay() and game_object.set_randomize_delay(self.np_random)
                game_object.decrease_delay_before_spawn()
                delay_spawn_objects.append(game_object)
                continue

            if game_object.require_points():
                if not positions:
                    warn(f'something wrong {game_object}''s is_respawnable()')
                    continue
                position = positions.pop()
                game_object.center = position
            short_id = self.id_manager.assign_short_id(game_object.uuid)

            if game_object.spawn_radius > 0:
                new_center = randomize_center(
                    self.np_random,
                    game_object.center,
                    game_object.spawn_radius)
                game_object.center = new_center

            if short_id < 0:
                warn('full')
                break
            if short_id in self.game_objects:
                # 사실 발생할 리가 없지만 그래도
                raise Exception(f"GameObject {short_id} already exists")
            game_object.set_short_id(short_id)
            self.game_objects[short_id] = game_object
            self._handle_register_object(game_object)
        delay_spawn_objects and self.pending_spawn_objects.extend(
            delay_spawn_objects)

    def _update_state_of_objects(self):
        for game_object in self.game_objects.values():
            states = game_object.get_states()
            states and self._handle_update_object(game_object, states)

    def _remove_objects(self):
        while self.removing_game_object_ids:
            game_object_id = self.removing_game_object_ids.pop()
            game_object: GameObject = self.game_objects.pop(
                game_object_id, None)
            if not game_object:
                continue
            self.id_manager.release_id(game_object.uuid, game_object.short_id)
            self._handle_remove_object(game_object)

    def _step_processing(self, actions: dict[int | str, list[ControlAction]]):
        for game_object in self.game_objects.values():
            game_object: GameObject
            if game_object.life < 1:
                self.removing_game_object_ids.append(game_object.short_id)
                continue
            if not isinstance(game_object, ActiveGameObject):
                continue
            object_actions = actions.get(game_object.short_id, [])
            object_actions and game_object.set_actions(object_actions)
            not game_object.act() and self.removing_game_object_ids.append(game_object.short_id)

    def _post_step_processing(self):
        pass
