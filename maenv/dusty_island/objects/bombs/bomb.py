import collections
from maenv.core.cardinal_direction import CardinalDirectionType
from maenv.core.objects.active_object import ActiveGameObject


class Bomb(ActiveGameObject):

    damage = None
    hitting_cooldown = None
    delay_cooldown = None
    active_duration = None
    min_range = None
    max_range = None

    def __init__(
        self,
        center: tuple[int, int],
        size: int,
        bomber_id: int,
        throw_gauge: float,
        direction_type: CardinalDirectionType
    ) -> None:
        super(Bomb, self).__init__(
            center,
            size,
            size,
            100,
            0,
        )
        self.bomber_id = bomber_id
        self.hitting_memory: dict[int, int] = collections.defaultdict(int)
        self.delay_count = self.delay_cooldown
        self.active_count = self.active_duration
        self.direction.set_direction(direction_type)
        if throw_gauge > 1:
            power = self.max_range
        else:
            power = (self.max_range - self.min_range) * throw_gauge
            power += self.min_range
        self.center += self.direction.get_vector() * power

    def is_activate(self):
        return self.delay_count < 1

    def hit(self, game_object_id: int) -> bool:
        if self.hitting_memory[game_object_id] > 0:
            return False
        self.hitting_memory[game_object_id] = self.hitting_cooldown
        return True

    def act(self) -> bool:
        if self.delay_count > 0:
            self.delay_count -= 1
            return True
        self.active_count -= 1
        return self.active_count > 0
