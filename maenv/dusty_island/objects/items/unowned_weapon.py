import maenv.utils.colors as colors
from maenv.core.objects.passive_object import PassiveGameObject
from maenv.dusty_island.objects.weapons import Weapon
from maenv.dusty_island.objects.items import PickUpItem


class UnOwnedWeapon(PickUpItem):

    render_color = colors.ORANGE

    def __init__(
        self,
        width: int,
        height: int,
        throw_limit: int,
        weapon_cls: type[Weapon],
        center=[0, 0],
        is_facing_right=False
    ) -> None:
        # tree Type에 따라 변경
        super(UnOwnedWeapon, self).__init__(
            width,
            height,
            center,
        )
        self.is_facing_right = is_facing_right
        self.throw_limit = throw_limit
        self.weapon_cls = weapon_cls

    def activate_weapon(self) -> Weapon:
        weapon = self.weapon_cls()
        weapon.throw_limit = self.throw_limit
        return weapon
