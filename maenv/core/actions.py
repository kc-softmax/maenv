from dataclasses import dataclass


@dataclass
class ControlAction:
    """
        각 env 마다 다른 action들을 가지고 있을것이다.
        상속받아 사용한다.
    """
    STOP = 1
    FORWARD = 2
    ROTATE_LEFT = 3
    ROTATE_RIGHT = 4

    # 유효성 검사해야한다.
