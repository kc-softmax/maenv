import math
import sys
import pygame
from maenv.utils.colors import (
    BETA_GRID,
    BLACK,
    BLUE
)
from maenv.core.direction import DirectionType
from maenv.core.actions import ControlAction, ActionType
from maenv.dusty_island.dusty_env import DustyEnv
from maenv.dusty_island.consts.actions import DustyActiveAction

if __name__ == '__main__':
    # TODO get args from sys.argv
    # select env and maps
    # currently only support dusty env
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    pygame.init()
    pygame.display.set_caption('maEnv')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont('Arial', 16)
    clock = pygame.time.Clock()

    player_agent_name = 'player'
    agent_names = ['player',
                   'bot_1', 'bot_2', 'bot3']

    env = DustyEnv(agent_names=agent_names)

    while True:
        player_actions: list[ControlAction] = []
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_actions.append(
                        ControlAction(
                            ActionType.ACTIVE,
                            DustyActiveAction.DEFAULT_SKILL_DOWN
                        ))
                if event.key == pygame.K_2:
                    player_actions.append(
                        ControlAction(
                            ActionType.ACTIVE,
                            DustyActiveAction.SPECIAL_SKILL_DOWN
                        ))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    player_actions.append(
                        ControlAction(
                            ActionType.ACTIVE,
                            DustyActiveAction.DEFAULT_SKILL_UP
                        ))
                if event.key == pygame.K_2:
                    player_actions.append(
                        ControlAction(
                            ActionType.ACTIVE,
                            DustyActiveAction.SPECIAL_SKILL_UP
                        ))

        event = pygame.key.get_pressed()
        if event[pygame.K_s]:
            if event[pygame.K_a]:
                direction = DirectionType.SW
            elif event[pygame.K_d]:
                direction = DirectionType.SE
            else:
                direction = DirectionType.S
            player_actions.append(ControlAction(
                ActionType.IMMEDIATE_CONTROL, direction))

        if event[pygame.K_w]:
            if event[pygame.K_a]:
                direction = DirectionType.NW
            elif event[pygame.K_d]:
                direction = DirectionType.NE
            else:
                direction = DirectionType.N
            player_actions.append(ControlAction(
                ActionType.IMMEDIATE_CONTROL, direction))

        if event[pygame.K_a] and not (event[pygame.K_w] or event[pygame.K_s]):
            direction = DirectionType.W
            player_actions.append(ControlAction(
                ActionType.IMMEDIATE_CONTROL, direction))

        if event[pygame.K_d] and not (event[pygame.K_w] or event[pygame.K_s]):
            direction = DirectionType.E
            player_actions.append(ControlAction(
                ActionType.IMMEDIATE_CONTROL, direction))

        if event[pygame.K_LEFT]:
            player_actions.append(
                ControlAction(
                    ActionType.ACTIVE,
                    DustyActiveAction.AIMING_LEFT
                ))
        if event[pygame.K_RIGHT]:
            player_actions.append(
                ControlAction(
                    ActionType.ACTIVE,
                    DustyActiveAction.AIMING_RIGHT
                ))
        actions = {}
        for agent_id, agent in env.agents.items():
            if agent.agent_name == player_agent_name:
                actions[agent_id] = player_actions
                # player
                if agent.weapon and agent.weapon.throwing:
                    mouse_pos = pygame.mouse.get_pos()
                    mouse_vector = pygame.Vector2(
                        mouse_pos[0] - agent.centerx,
                        mouse_pos[1] - agent.centery
                    ).normalize()
                    pygame.draw.line(
                        surface, BLUE,
                        agent.center, mouse_vector * 32, 10)
            else:
                actions[agent_id] = []
        _, _, terminateds, _, _ = env.step(actions)

        if terminateds['__all__']:
            sys.exit()

        surface = env.render(SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.blit(surface, (0, 0))

        pygame.display.update()
