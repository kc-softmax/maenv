import uuid
import pygame
import math
import warnings
from collections import deque
from maenv.core.objects.game_object import GameObject
from maenv.core.cardinal_direction import CardinalDirection, CardinalDirectionType
from maenv.core.actions import ControlAction


class ActiveGameObject(GameObject):

    direction_system = CardinalDirection
    vision_range = 1
    damage = 0

    def __init__(
        self,
        center: tuple[int, int],
        width: int,
        height: int,
        life: int,
        speed: int,
    ) -> None:
        super(ActiveGameObject, self).__init__(
            center[0],
            center[1],
            width,
            height,
            life)
        self.paths: deque[pygame.math.Vector2] = deque(maxlen=5)
        self.is_move_cancelled = False
        self.moved = False
        self.direction = self.direction_system()
        self.speed: int = math.floor(speed)
        self.owner_uuid: uuid.UUID = None
        self.actions: list[ControlAction] = []

    def move(self):
        next_point = self.center + self.direction.get_vector() * self.speed
        self.center = next_point
        self.paths.appendleft(next_point)

    def cancel_movement(self):
        if self.is_move_cancelled:
            self.is_move_cancelled = False
            if len(self.paths) > 1:
                self.paths.popleft()
                self.center = self.paths[0]

    def handle_actions(self, action: any):
        warnings.warn(
            f'{action} is coming in abstract handle_action, but not implemented handle_action or may be called super()'
        )

    def set_actions(self, actions: list[ControlAction]):
        self.actions = actions

    def follow_direction(self, direction: CardinalDirection):
        if not isinstance(direction, self.direction_system):
            raise Exception('check direction type, via directions')
        self.direction = direction

    def update_direction(self, direction_type: CardinalDirectionType):
        self.direction.set_direction(direction_type)

    def act(self) -> bool:
        move = False
        while self.actions:
            action = self.actions.pop()
            match action:
                case ControlAction.STOP:
                    move = False
                case ControlAction.FORWARD:
                    move = True
                case ControlAction.ROTATE_LEFT:
                    self.direction.rotate_ip(False)
                case ControlAction.ROTATE_RIGHT:
                    self.direction.rotate_ip(True)
                case _:
                    self.handle_actions(action)
        self.direction.update()
        move and self.move()
        self.moved = move
        return True
