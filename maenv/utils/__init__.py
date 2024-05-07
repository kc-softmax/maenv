import math
import numpy as np


def get_distance(src: tuple[int, int], dst: tuple[int, int]):
    return math.hypot(
        src[0] - dst[0],
        src[1] - dst[1])


def randomize_center(
    np_random: np.random.Generator,
    origin_center: tuple[int, int],
    spawn_radius: int
):
    # 원점에서 spawn_nearby_distance 거리 내의 랜덤 위치를 계산
    angle = np_random.uniform(0, 2 * np.pi)  # 0에서 2π 사이의 랜덤한 각도
    radius = np_random.uniform(
        0, spawn_radius)  # 0에서 최대 거리까지의 랜덤한 반지름

    # 극좌표를 직교좌표로 변환
    dx = radius * np.cos(angle)
    dy = radius * np.sin(angle)

    # 원래 중심점에 랜덤 변화를 추가
    new_center = (origin_center[0] + dx, origin_center[1] + dy)
    return new_center
