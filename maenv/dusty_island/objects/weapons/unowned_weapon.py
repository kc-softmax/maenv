import maenv.utils.colors as colors
from maenv.core.objects.passive_object import PassiveGameObject
from maenv.core.state import ObjectState
from maenv.dusty_island.objects.weapons import Weapon
from maenv.dusty_island.consts.game import (
    WEAPON_PICKUP_DURATION
)


class UnOwnedWeapon(PassiveGameObject):

    render_color = colors.ORANGE

    def __init__(
        self,
        width: int,
        height: int,
        throw_limit: int,
        weapon_cls: type[Weapon],
        center=[0, 0]
    ) -> None:
        # tree Type에 따라 변경
        super(UnOwnedWeapon, self).__init__(
            center,
            width,
            height,
            1
        )
        self.throw_limit = throw_limit
        self.weapon_cls = weapon_cls
        self.pickup_candidate_map: dict[int, int] = {}
        self.pickup_expect_map: dict[int, int] = {}
        self.owner_id = -1

    def activate_weapon(self) -> Weapon:
        weapon = self.weapon_cls()
        weapon.throw_limit = self.throw_limit
        return weapon

    def collide_with_dusty(self, dusty_id: int):
        if dusty_id not in self.pickup_candidate_map:
            # 새로 줍기 시작한다.
            self.pickup_candidate_map[dusty_id] = 0
            self.pickup_expect_map[dusty_id] = 0
            self.update_state(
                ObjectState.START_PICKUP,
                dusty_id,
                WEAPON_PICKUP_DURATION
            )
            # new dusty
        self.pickup_candidate_map[dusty_id] += 1
        if self.pickup_candidate_map[dusty_id] > WEAPON_PICKUP_DURATION:
            self.owner_id = dusty_id
            self.life = 0

    def update_object(self):
        super().update_object()
        pickup_failed_ids = []
        for pickup_id in self.pickup_expect_map:
            self.pickup_expect_map[pickup_id] += 1
            if pickup_id not in self.pickup_candidate_map:
                pickup_failed_ids.append(pickup_id)
            else:
                if (
                    self.pickup_candidate_map[pickup_id] !=
                    self.pickup_expect_map[pickup_id]
                ):
                    pickup_failed_ids.append(pickup_id)
        for failed_pickup_id in pickup_failed_ids:
            self.pickup_candidate_map.pop(failed_pickup_id)
            self.pickup_expect_map.pop(failed_pickup_id)
            self.update_state(
                ObjectState.CANCEL_PICKUP,
                failed_pickup_id,
            )
