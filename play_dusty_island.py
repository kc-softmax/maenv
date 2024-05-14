import math
import sys
import pygame
from maenv.dusty_island.dusty_env import DustyEnv
from maenv.dusty_island.consts.actions import DustyControlAction

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
        player_actions = []
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_actions.append(
                        DustyControlAction.DEFAULT_SKILL_DOWN)
                if event.key == pygame.K_2:
                    player_actions.append(
                        DustyControlAction.SPECIAL_SKILL_DOWN)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    player_actions.append(
                        DustyControlAction.DEFAULT_SKILL_UP)
                if event.key == pygame.K_2:
                    player_actions.append(
                        DustyControlAction.SPECIAL_SKILL_UP)

        event = pygame.key.get_pressed()
        if event[pygame.K_DOWN]:
            player_actions.append(DustyControlAction.STOP)
        if event[pygame.K_UP]:
            player_actions.append(DustyControlAction.FORWARD)
        if event[pygame.K_LEFT]:
            player_actions.append(DustyControlAction.ROTATE_LEFT)
        if event[pygame.K_RIGHT]:
            player_actions.append(DustyControlAction.ROTATE_RIGHT)
        # if event[pygame.K_w]:
        #     player_actions.append(ControlAction.ACTIVE_SKILL_2)
        # if event[pygame.K_1]:
        #     player_actions.append(ControlAction.SPECIAL_SKILL_1)
        # if event[pygame.K_2]:
        #     player_actions.append(ControlAction.SPECIAL_SKILL_2)
        # if event[pygame.K_3]:
        #     player_actions.append(ControlAction.SPECIAL_SKILL_3)
        # if event[pygame.K_4]:
        #     player_actions.append(ControlAction.SPECIAL_SKILL_4)

        actions = {}
        for agent_id, agent in env.agents.items():
            if agent.agent_name == player_agent_name:
                actions[agent_id] = player_actions
            else:
                actions[agent_id] = [DustyControlAction.STOP]

        _, _, terminateds, _, _ = env.step(actions)

        if terminateds['__all__']:
            sys.exit()

        surface = env.render(SCREEN_WIDTH, SCREEN_HEIGHT)
        screen.blit(surface, (0, 0))

        pygame.display.update()
