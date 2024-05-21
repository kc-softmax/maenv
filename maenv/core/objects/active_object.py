import uuid
import pygame
import math
import warnings
from collections import deque
from pygame.math import Vector2
from maenv.core.objects.game_object import GameObject
from maenv.core.state import ObjectState
from maenv.core.direction import DirectionType, Direction
from maenv.core.actions import ControlAction, ActionType, WheelAction


class ActiveGameObject(GameObject):

    is_wheel_direction = False
    vision_range = 1

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
        self.target: GameObject = None
        self.is_move_cancelled = False
        self.moved = False
        self.knockback_count = 0
        self.force_direction_vector: Vector2 = None
        self.direction = Direction(self.is_wheel_direction)
        self.speed: int = math.floor(speed)
        self.owner_id: int = None
        self.actions: list[ControlAction] = []

    def update_state(self, state: ObjectState, target: GameObject = None, value: any = None):
        super().update_state(state, target, value)
        if state == ObjectState.KNOCKBACK and isinstance(target, ActiveGameObject) and value > 0:
            self.force_direction_vector = target.direction.get_vector()
            self.knockback_count = value

    def move(self):
        if self.force_direction_vector:
            direction_vector = self.force_direction_vector
        else:
            direction_vector = self.direction.get_vector()
        next_point = self.center + direction_vector * self.speed
        self.center = next_point

    def set_target(self, target: GameObject):
        if target != self.target:
            self.update_state(ObjectState.TARGETING, target)
        self.target = target

    def get_target_vector(self) -> pygame.Vector2 | None:
        if self.target:
            return pygame.Vector2(
                self.target.centerx - self.centerx,
                self.target.centery - self.centery,
            ).normalize()
        return None

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

    def follow_direction(self, direction: Direction):
        self.direction = direction

    def update_direction(self, direction_type: DirectionType):
        self.direction.set_direction(direction_type)

    def handle_wheel_action(self, action: WheelAction) -> bool:
        match action:
            case WheelAction.ROTATE_LEFT:
                self.direction.rotate_ip(False)
            case WheelAction.ROTATE_RIGHT:
                self.direction.rotate_ip(True)
            case WheelAction.STOP:
                return False
        return True

    def handle_immediate_action(self, action: DirectionType) -> bool:
        self.direction.set_direction(DirectionType(action))
        return True

    def act(self):
        move = False
        while self.actions:
            action = self.actions.pop()
            action_type = action.action_type
            action_value = action.action_value
            match action_type:
                case ActionType.WHEEL_CONTROL:
                    assert self.is_wheel_direction
                    move = self.handle_wheel_action(action_value)
                case ActionType.IMMEDIATE_CONTROL:
                    assert not self.is_wheel_direction
                    move = self.handle_immediate_action(action_value)
                case ActionType.ACTIVE:
                    self.handle_actions(action_value)

        self.direction.update()

        # 일단 knockback에 의한 이동과 일반적인 이동을 분리하여 처리한다.
        if self.knockback_count > 0:
            self.knockback_count -= 1
            if self.knockback_count < 1:
                # 버그가 발생할 수도 있다. force direciton 이 knockback에 의한 것이 아닐수도 있기 때문에
                self.force_direction_vector = None
            move = True

        move and self.move()
        self.moved = move
        self.paths.appendleft((self.centerx, self.centery))
